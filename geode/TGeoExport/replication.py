# -*- coding: utf8 -*-

from math import degrees as to_degrees  # TODO
import ROOT
import logging

def get_axis_encoding_number_from( obj, attrs ):
    code = None
    attrName = None
    value = None
    for cAttr, cCode in attrs.iteritems():
        getterName = 'get_' + cAttr
        val = float(getattr( obj, getterName )()) if getattr( obj, getterName ) else None
        if val and val > 0:
            if not attrName:
                attrName = cAttr
                value = getattr( obj, getterName )()
                code = cCode
            else:
                raise ValueError( 'Only one axis should be specified for '
                    'direction. Got at least "%s" and "%s"'%(
                    attrName, cAttr ) )
    return code, attrName, value

def get_axis_encoding_number( v3Struct ):
    """
    ROOT division algorithm refers to encoded directions. It is hardcoded
    somewhere that for cartesian type directions, the code correspondence is
    x -> 1, y -> 2, z -> 3 while for polar type codes are rho ->1, phi -> 2.
    Here we will check components in order and return index of first non-null
    component starting from 1.
    Operates with extGDML `directionType' class instance.
    """
    cartesianAssumed, cartNm, cartLength = get_axis_encoding_number_from( v3Struct,
            { 'x' : 1,    'y' : 2,    'z' : 3 } )
    polarAssumed, polNm, polLength = get_axis_encoding_number_from( v3Struct,
            { 'rho' : 1,  'phi' : 2 } )
    if cartesianAssumed and polarAssumed:
        raise ValueError( 'Only one axis should be specified for '
                    'direction. Got at least "%s" and "%s"'%(
                    cartNm, polNm ) )
    elif not (cartesianAssumed or polarAssumed):
        raise ValueError( 'Could not find out axis direction.' )
    axisType = 'cartesian'
    axisName = cartNm
    code = cartesianAssumed
    val = cartLength
    if polarAssumed:
        axisType = 'polar'
        axisName = polNm
        code = polarAssumed
        val = polLength
    return code, axisName, axisType, val

def replicate(I, gdmlNode, volume):
    L = logging.getLogger(__name__)
    # parameters dict to be updated:
    p = {}
    # resolve replicable volume:
    replicableVol = I.get_volume(gdmlNode.get_volumeref().get_ref())
    # resolve replication algorithm:
    algorithm = gdmlNode.get_ReplicationAlgorithm()
    # note, that current GDML schema (3.1.4 up to the 10, Oct, 016)
    # only supports the replication along axis.
    if not 'AxisReplicationAlgorithmType' == algorithm.__class__.__name__:
        raise ValueError( "Current release doesn't support "
                          "replication other than "
                          '"AxisReplicationAlgorithmType".' )
    # The differences between Geant4 replication mechanics and ROOT dividing:
    #  1) Replication in Geant4 preserves the original volume (it keeps
    #     existing in some way on scene) while in ROOT one have to override
    #     dividing one with divided one.
    #  2) ROOT division does not places any replicated entities inside divided
    #     volume. That should be done after within AddNode.
    #  3) start&step values differs. While in Geant4 it refers to number of
    #     replicas, root division start&step should be expressed in real
    #     numbers (length or angular).
    #  3*) Geant4 doesn't still (ver. 4.9.6) support these copy_num_start=""
    #     and copy_num_step="" attributes anyway!

    # get the direction description in form:
    # [ <root axis code>, <txt axis name>,
    #           ['cartesian'/'polar'], <length of axis> ]
    dirDescr = get_axis_encoding_number( algorithm.get_direction() )

    # todo: if these are planned to be supported by G4 at some time, we'll
    # delete this warning:
    if I.E.evaluate(gdmlNode.get_copy_num_start()) != 1 \
     or I.E.evaluate(gdmlNode.get_copy_num_step()) != 1:
        L.error( "(unsupported feature) For replica volume \"%s\": "
            "copy_num_start=%d copy_num_step=%d; Geant4 of versions of at "
            "least <=4.9.6 does not support these attributes.\n"%(
            volume.GetName(), nStart, nStep )  )

    # Now convert according to 3) the start and step:
    rlo, rhi = ROOT.Double(), ROOT.Double()
    volume.GetShape().GetAxisRange( dirDescr[0], rlo, rhi )
    # Now, compute division parameters:
    nStart  = I.E.eval_int(gdmlNode.get_copy_num_start())
    nStep   = I.E.eval_int(gdmlNode.get_copy_num_step())
    N       = I.E.eval_int( gdmlNode.get_number() )
    # this calculation currently has no sense since Geant4 ignored copy_num_*
    # attributes of replicavol. Actual step is obtained within <width/> and
    # <offset/> values of sub-elements.
    #posStpSingle = nStep*( rhi - rlo )/N

    # As for Geant-4.9.6 the <offset/> sub-element also has only sense for
    # radial replicating axis --- cartesian offset is not applied.
    offsetVal =  algorithm.get_offset().get_numerical_value( I.E )
    widthVal  =  algorithm.get_width().get_numerical_value( I.E )

    # todo: if Geant4 will take into account offset for cartesian replicas,
    # this warning may be changed.
    if offsetVal != 0. and 'cartesian' == dirDescr[2]:
        L.error("(unsupported feature) For replication along Cartesian "
            "axis direction, Geant4 doesn't consider attribute \"offset\" "
            "which is specified for replicavol \"%s\" = %e.\n"%(
            volume.GetName(), offsetVal) )

    # todo: Degree-crutch
    if 'polar' == dirDescr[2]:
        offsetVal = to_degrees(offsetVal)
        widthVal  = to_degrees(widthVal)

    rargs = [ volume.GetName(),             # const char * divname
              dirDescr[0],                  # Int_t iaxis
              N,                            # Int_t ndiv
              offsetVal - (N*widthVal)/2,   # Double_t start
              widthVal,                     # Double_t step
              volume.GetMedium().GetId()    # Int_t numed
            ]
    xlo, xhi = ROOT.Double(0), ROOT.Double(0)
    rng = volume.GetShape().GetAxisRange( rargs[1], xlo, xhi )  # XXX
    L.debug( 'division args: %s, axis range [%e:%e]'%(str(rargs), xlo, xhi) )
    dvd = volume.Divide( *rargs )
    # Add childs into divided volume here:
    #if volume.GetNdaughters():
    #    dvd.ReplayCreation( volume )
    dvd.AddNode( replicableVol, 1, 0 )
    return dvd

