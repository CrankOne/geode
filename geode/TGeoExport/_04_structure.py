# -*- coding: utf8 -*-

"""
File describes routines for conversion the GDML structure hierarchy definition
into corresponding ROOT TGeo instances.

Shouldn't be used as a separate module. Import extGDML.root.bindings instead.
"""

import ROOT
from .replication import replicate
from .refResolve import get_or_resolve_position, get_or_resolve_rotation  # get_or_resolve_scale
import logging
from os.path import splitext, basename

def make_physvol_from_solids( I, subVol, volume, *args, **kwargs ):
    subVolInstance = None
    # subVol contains either <file/> (w FileReferenceType),
    # either <volumeref/> reference. Other attrs/subels:
    #   els: position[ref], rotation[ref], scale[ref],
    #   attr: name
    #   attr: copynumber
    if subVol.get_file():
        from geode.gdmlFileExport import export_gdml_file
        submoduleFilename = subVol.get_file().get_name()
        sumoduleName = splitext(basename(submoduleFilename))[0]
        # No need:
        #subIdx = I.new_subindex( 'include-' + sumoduleName )
        subIdx = I
        auxResults = {}
        submoduleKWargs = {
                'verboseParse'   : kwargs.get('verboseParse', True),
                'verboseConvert' : kwargs.get('verboseConvert', True),
                'index' : subIdx, 'indexClass' : None,
                'finalizeGeometry' : False,
                'exportFormat' : 'ROOT',
                'setupName' : 'Default',
                'auxResults' : auxResults
            }
        try:
            export_gdml_file( submoduleFilename, **submoduleKWargs )
        except:
            L.warning( '(exception addendum) '
                    'While exporting the file \"%s\":\n'%submoduleFilename )
            raise
        # Note: volname attr
        volname = subVol.get_file().get_volname()
        if volname:
            # Note: volume from "Default" setup is taken when volname=""
            # attr is not provided.
            subVolInstance = I.get_volume( volname )
        elif auxResults.get('topVolume', None):
            subVolInstance = auxResults['topVolume']

        if not subVolInstance:
            raise RuntimeError('Reading of "%s" did not yielded unique top '
                    'volume. It should be defined either as attribute of '
                    '"volname" <file/> element, either referred in "Default" '
                    '<setup/>.'%submoduleFilename )
        # TODO: when there is only one <setup/> in a file, Geant4 seems to
        # also take it as a current setup.
    elif subVol.get_volumeref():
        subVolInstance = I.get_volume( subVol.get_volumeref().get_ref() )
    else:
        raise ValueError('Bad state --- physvol did not referenced '
            'to a file or volumeref.' )
    position = get_or_resolve_position( subVol, I, default=None )
    rotation = get_or_resolve_rotation( subVol, I, default=None )
    #scale = get_or_resolve_scale( subVol, default=None )
    T = ROOT.TGeoGenTrans()
    if rotation:
        T.SetRotation( rotation[1] )
    if position:
        T.SetTranslation( position[1].GetTranslation() )
    #if scale:
    #    T.SetScale( scale )
    volume.AddNode( subVolInstance, 1, T )  # TODO: translations mx

def read_structure( gdml, I,
                    quiet=False, *args, **kwargs ):
    """
    This function works with <structure/> section of GDML document performing
    creation of logical volumes consisting of hierarchy of previously defined
    solids with assigned materials and placement parameters
    (position/rotation).
    """
    from .loop import treat_loop_element
    # structure includes:
    #   1. <volume/>
    #   2. <assembly/>  (TODO)
    #   3. <loop/>  (TODO)
    #   4. ParameterisedAlgorithm ref (TODO)
    for volume in gdml.get_structure().get_volume():
        # VolumeType <- IdentifableVolumeType:
        # parent (IdentifableVolumeType):
        #   <file/> / <columeref/>
        #   <position/> / <positionref/>
        #   <rotation/> / <rotationref/>
        #   <scale/> / <scaleref/>
        # own:
        #   <materialref/> 
        #   <solidref/>
        #   <physvol/> / <divisonvol/> / <replicavol/> / <paramvol/>
        mediumObj = None
        # only referencing to material is allowed here (inline is forbidden)
        matName = volume.get_materialref().get_ref()
        matObj = I.get_material( matName )
        assert( matObj )
        # only referencing to solid is allowed here (inline is forbidden)
        solidObj = I.get_solid( volume.get_solidref().get_ref() )
        # Now, get (or create, if need) a medium:
        mediumObj = I.get_medium( matName, noexcept=True )
        if mediumObj is None:
            mediumObj = ROOT.TGeoMedium( matName, I.get_media_count(), matObj )
            L.debug( 'New medium object %s created.'%str(mediumObj) )
            #if not quiet:
            #    mediumObj.Print()  # TODO: L.debug()
            # TODO: ^^^ TGeoMedium supports a set of additional parameters
            # which may refer to Geant4 material properties (temperature,
            # permeability, etc).
            I.set_medium( mediumObj, name=matName )

        # Now make a TGeoVolume:
        volumeObj = ROOT.TGeoVolume( volume.get_name(), solidObj, mediumObj )
        I.set_volume( volumeObj, name=volume.get_name() )

        if volume.get_physvol():
            for subVol in volume.get_physvol():
                make_physvol_from_solids( I, subVol, volumeObj,
                                          *args, **kwargs )
        elif volume.get_replicavol():
            replicate( I, volume.get_replicavol(),
                                   volumeObj )
            # We need to keep reference to the parent volume in order to
            # prevent python garbage collector from clearing object
            # that ROOT may use somewhere.
            I.set_volume( I.get_volume(volume.get_name()), name='@divided-' + volume.get_name() )
            I.set_volume( volumeObj, name=volume.get_name(), override=True )
        elif volume.get_divisionvol():
            # TODO
            raise NotImplementedError( '<divisionvol/> is not yet supported.' )
        elif volume.get_paramvol():
            # TODO
            raise NotImplementedError( '<paramvol/> is not yet supported.' )
        #I.set_volume( volumeObj, name=volume.get_name() )
        # loopedElement = volume.get_loop().get_physvol()
        for l in volume.get_loop():
            treat_loop_element( I, l,
                    lambda l: [make_physvol_from_solids( I, e, volumeObj, \
                                *args, **kwargs ) for e in l.get_physvol()],
                    context=volume.__class__.__name__ )
        # TODO: auxiliary
    # TODO: assembly
    def _loop_callback( lastLoopNode ):
        # TODO: lastLoopNode.get_volume()
        raise NotImplementedError('Loop in <structure/> is not yet supported.')
    for l in gdml.get_structure().get_loop():
        treat_loop_element( I, l, _loop_callback,
                context=gdml.get_structure().__class__.__name__ )
    # TODO: ParameterisationAlgorithm
