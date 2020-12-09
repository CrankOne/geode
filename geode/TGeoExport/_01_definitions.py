# -*- coding: utf8 -*-

"""
File describes routines for conversion the GDML definitions into corresponding
ROOT structures.

Shouldn't be used as a separate module. Import `geode.TGeoExport.bindings' instead.
"""

import ROOT
import logging

def constant_to_root_struct( gdmlNode, E, defStruct ):
    defStruct.name  = gdmlNode.get_name()
    defStruct.value = gdmlNode.get_numerical_value( E )

def scalar_quantity_to_root_struct( gdmlNode, E, qStruct ):
    qStruct.absoluteValue = gdmlNode.get_numerical_value( E )
    qStruct.value = gdmlNode.measuredVal
    qStruct.name  = gdmlNode.get_name()
    qStruct.unit  = gdmlNode.get_unit()
    qStruct.qType = gdmlNode.get_type()

def vector_quantity_to_root_struct( gdmlNode, E, v3Struct ):
    v3Struct.components[0],             \
        v3Struct.components[1],         \
        v3Struct.components[2] = gdmlNode.get_evaluated_components( E )
    v3Struct.computedComponents[0],     \
        v3Struct.computedComponents[1], \
        v3Struct.computedComponents[2] = gdmlNode.get_absolute_components( E )
    if hasattr(gdmlNode, 'get_name'):
        v3Struct.name = gdmlNode.get_name()
    else:
        v3Struct.name = ''
    v3Struct.unit = gdmlNode.get_unit() or '<none>'
    v3Struct.qType = gdmlNode.get_type() or '<none>'

def rotation_from_v3( v3r ):
    rot = None
    if str(v3r.name):
        rot = ROOT.TGeoRotation(v3r.name)
    else:
        rot = ROOT.TGeoRotation()
    rot.RotateZ( -v3r.components[2] )
    rot.RotateY( -v3r.components[1] )
    rot.RotateX( -v3r.components[0] )
    #nativeRot = ROOT.TRotation()
    #nativeRot.RotateX( -v3r.components[0]/2 )
    #nativeRot.RotateY(  v3r.components[1] )
    #nativeRot.RotateZ( -v3r.components[2] )
    #rot.SetAngles(
    #        nativeRot.GetXPhi(),
    #        nativeRot.GetXTheta(),
    #        nativeRot.GetXPsi()
    #    )
    return rot

def position_from_v3( v3p ):
    kws = [ v3p.computedComponents[0],
            v3p.computedComponents[1],
            v3p.computedComponents[2] ]
    if str(v3p.name):
        kws.insert(0, v3p.name)
    return ROOT.TGeoTranslation( *kws )

def scale_from_v3( v3s ):
    kws = [ v3s.components[0],
            v3s.components[1],
            v3s.components[2]]
    if str(v3s.name):
        kws.insert(0, v3s.name)
    return ROOT.TGeoScale( *kws )

# def scale_from_v3( v3p )

def read_definitions( gdml, I,
                      quiet=False, *args, **kwargs ):
    """
    This function performs creating and filling ROOT TTrees with definitions
    found in <define/> section of GDML document: constants, variables,
    quantities, positions, rotation and matrices.
    It will create at the current TFile object following TTree instances:
        - Values (where constants and variables are placed)
        - Quantities (where all named scalar quantities are placed)
        - Positions
        - Rotations
        - Matrices (unimplemented, TODO)
    All the constants and variables will not be indexed in `defs' dictionary
    since their definitions will be forwarded directly to CLHEP evaluator
    instance. However they can be useful for consuming ROOT routines, so we
    placed them into TTrees for user inspection.
    """
    from geode.TGeoExport.loop import treat_loop_element

    L = logging.getLogger(__name__)

    # Note for PyROOT 6.22 update: AddressOf() is now called AddressOf()
    AOF = getattr(ROOT, 'addressof', None)
    if AOF is None:
        AOF = ROOT.AddressOf

    defStruct = ROOT.Definition_t()
    rTree = ROOT.TTree('Values', 'Named constants & variables.')
    rTree.Branch( 'value', defStruct, 'value/D' )
    rTree.Branch( 'name',  AOF(defStruct, 'name'), 'name[128]/C' )

    #
    # Constants:
    for cst in gdml.get_define().get_constant():
        constant_to_root_struct( cst, I.E, defStruct )
        L.debug( "cst: %s=%s"%(defStruct.name, defStruct.value) )
        rTree.Fill()

    #
    # Variables:
    for var in gdml.get_define().get_variable():
        constant_to_root_struct( var, I.E, defStruct )
        L.debug( "var: %s=%s"%(defStruct.name, defStruct.value) )
        rTree.Fill()

    if not quiet:
        rTree.Print()
    rTree.Write()

    qStruct = ROOT.ComputedQuantity_t()
    rTree = ROOT.TTree('Quantities', 'Named scalar quantities.')
    rTree.Branch( 'value',          qStruct, 'value/D' )
    rTree.Branch( 'absoluteValue',  qStruct, 'absoluteValue/D' )
    rTree.Branch( 'name',   AOF(qStruct, 'name'),    'name[128]/C' )
    rTree.Branch( 'unit',   AOF(qStruct, 'unit'),    'unit[32]/C'  )
    rTree.Branch( 'qType',  AOF(qStruct, 'qType'),   'qType[64]/C' )

    #
    # Quantities:
    for q in gdml.get_define().get_quantity():
        destStr = ROOT.ComputedQuantity_t()
        scalar_quantity_to_root_struct( q, I.E, destStr )
        # Note: since CINT-generated structs and classes seems to use
        # a trivial substitution instead of copy-ctr/assignment operator,
        # we did manual copying of members here. If there will be written:
        #qStruct = destStr
        # the qStruct reference will refer to destStr instance instead of
        # making a copy.
        qStruct.value = destStr.value
        qStruct.absoluteValue = destStr.absoluteValue
        qStruct.name = destStr.name
        qStruct.unit = destStr.unit
        qStruct.qType = destStr.qType
        L.debug( "q:%s=%s(%s)=%s"%(qStruct.name, qStruct.value, \
                                        qStruct.unit, qStruct.absoluteValue) )
        rTree.Fill()
        I.set_quantity( destStr, name=q.get_name() )

    if not quiet:
        rTree.Print()
    rTree.Write()

    v3Struct = ROOT.Vector3_t()
    rTree = ROOT.TTree('Positions', 'Named 3-component quantities: positions.' )
    rTree.Branch( 'components',      qStruct, 'components[3]/D' )
    rTree.Branch( 'computedComponents', qStruct, 'computedComponents[3]/D' )
    rTree.Branch( 'name',  AOF(qStruct, 'name'), 'name/C' )
    rTree.Branch( 'unit',  AOF(qStruct, 'unit'), 'unit/C' )
    rTree.Branch( 'qType', AOF(qStruct, 'qType'), 'qType/C' )

    #
    # Positions:
    for p in gdml.get_define().get_position():
        destStr = ROOT.Vector3_t()
        vector_quantity_to_root_struct( p, I.E, destStr )
        v3Struct = destStr
        L.debug( '%s pos: %s {%e, %e, %e} (%s) = {%e, %e, %e}'%(
            v3Struct.qType,
            v3Struct.name,
            v3Struct.components[0],
            v3Struct.components[1],
            v3Struct.components[2],
            v3Struct.unit,
            v3Struct.computedComponents[0],
            v3Struct.computedComponents[1],
            v3Struct.computedComponents[2] ) )
        rTree.Fill()
        I.set_position( (destStr, position_from_v3(destStr)),
                        name=p.get_name() )

    if not quiet:
        rTree.Print()
    rTree.Write()

    rTree = ROOT.TTree('Rotatitions', 'Named 3-component quantities: rotations.')
    rTree.Branch( 'components',      qStruct, 'components[3]/D' )
    rTree.Branch( 'computedComponents', qStruct, 'computedComponents[3]/D' )
    rTree.Branch( 'name',  AOF(qStruct, 'name'), 'name/C' )
    rTree.Branch( 'unit',  AOF(qStruct, 'unit'), 'unit/C' )
    rTree.Branch( 'qType', AOF(qStruct, 'qType'), 'qType/C' )

    #
    # Rotations:
    for r in gdml.get_define().get_rotation():
        destStr = ROOT.Vector3_t()
        vector_quantity_to_root_struct( r, I.E, destStr )
        v3Struct = destStr
        L.debug( '%s rot: %s {%e, %e, %e} (%s) = {%e, %e, %e}'%(
                v3Struct.qType,
                v3Struct.name,
                v3Struct.components[0],
                v3Struct.components[1],
                v3Struct.components[2],
                v3Struct.unit,
                v3Struct.computedComponents[0],
                v3Struct.computedComponents[1],
                v3Struct.computedComponents[2] ) )
        rTree.Fill()
        I.set_rotation( (destStr,
                         rotation_from_v3(destStr)), name=r.get_name() )
    if not quiet:
        rTree.Print()
    rTree.Write()

    rTree = ROOT.TTree('Scales', 'Named 3-component quantities: scales.')
    rTree.Branch( 'components',      qStruct, 'components[3]/D' )
    rTree.Branch( 'name',  AOF(qStruct, 'name'), 'name/C' )

    #
    # Scales: scale_from_v3
    for s in gdml.get_define().get_scale():
        destStr = ROOT.Vector3_t()
        vector_quantity_to_root_struct( s, I.E, destStr )
        v3Struct = destStr
        L.debug( 'scale: %s {%e, %e, %e}'%(
                v3Struct.name,
                v3Struct.components[0],
                v3Struct.components[1],
                v3Struct.components[2] ) )
    if not quiet:
        rTree.Print()
    rTree.Write()

    # TODO: ... matrices

    for l in gdml.get_define().get_loop():
        treat_loop_element( I, l, context=gdml.get_define().__class.__name__ )
