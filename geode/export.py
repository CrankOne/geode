import logging
import importlib

import geode.GDMLParser.v3_1_6.classes as GDML  # TODO: ARG

def build_root_GDML( assemblyItems
                   , lib
                   , worldVol=None
                   , file_resolver=None
                   ):
    """
    Produces a root GDML document node defining setup built from multiple
    assembly files. It is somewhat common and simplistic case for setup in
    box-shaped "world" volume filled with air. Consider this as a boilerplate
    function for more specific cases (e.g. vacuumed cylinder or whatever).

    Provided `assemblyItems' must be a list of dictionaries with:
        * `geometry' argument referencing the GDML file (module) to include
        * `placement' to be a list or tuple of six elements, corresponding to
        position (3) and rotation (3) of the assembly
        * optionally, `posUnit` and `rotUnit' may denote units used for the
        `placement' argument, corresponding to position and rotation units
        (if not given, `mm' and `deg' will be implied).
    Returned is the instance of `GDML.gdml' class that may be then directly
    exported into GDML ASCII with its `export()` method.

    The `worldVol' must contain following fields:
        * `solidName' defining the name of world volume (optional, "solidWorld"
        will be used if not given)
        * `x, `y', `z' defining width, height and depth of the world box
        * `lunit' defining length units for `x', `y', `z'
    If `worldVol is not given, the cube 1x1x1m will be used.

    The `file_resolver' is `None' or a callable that accepts (lib entry,
    item key, item parameters) and returns an URI string that must be a name
    of the `<file/>' GDML tag.
    """
    L = logging.getLogger(__name__)
    if worldVol is None:
        worldVol = { 'x': 1, 'y': 1, 'z': 1, 'lunit': 'm' }
    if not file_resolver:
        file_resolver = lambda x, entryName, cfgParameters: x['file']
    # Build the setup object from YAML definitions
    solids = GDML.solids()
    defines = GDML.defineType()
    materials = GDML.materials()
    # - create world volume (TODO: take dimensions from a config)
    solidWorld = GDML.box( name=worldVol.get("solidName", "solidWorld")
                         , x=worldVol['x']
                         , y=worldVol['y']
                         , z=worldVol['z']
                         , lunit=worldVol['lunit'] )
    solids.add_Solid(solidWorld)
    worldVol = GDML.VolumeType( name="World"
                              , materialref=GDML.ReferenceType(ref='G4_AIR')
                              , solidref=GDML.ReferenceType(ref=solidWorld.get_name())
                              )
    # - iterate over enumerated entries, emplacing the definitions into structure
    # as <file/> instances with certain placements
    for k, cfgPs in assemblyItems:
        if 'geometry' not in cfgPs:
            L.error('The assembly "%s" does not request any geometry. Skip.'%k)
            continue
        geoPath = tuple(cfgPs['geometry'].split('/'))
        if geoPath not in lib.items:
            L.error('No geometry "%s" referenced by "%s" assembly. Skip.'%(
                cfgPs['geometry'], k))
            continue
        # -- create named position/rotation for reference
        position = GDML.positionType( name='position_%s'%k
                                    , x=cfgPs['placement'][0]
                                    , y=cfgPs['placement'][1]
                                    , z=cfgPs['placement'][2]
                                    , unit=cfgPs.get('posUnit', 'mm')
                                    , type_='cartesian'
                                    )
        rotation = GDML.positionType( name='rotation_%s'%k
                                    , x=cfgPs['placement'][3]
                                    , y=cfgPs['placement'][4]
                                    , z=cfgPs['placement'][5]
                                    , unit=cfgPs.get('rotUnit', 'deg')
                                    , type_='cartesian'
                                    )
        defines.add_position( position )
        defines.add_rotation( rotation )
        # put the assembly at certain position
        endpoint = file_resolver( lib.items[geoPath], k, cfgPs )
        placementDict = { 'file' : GDML.FileReferenceType( name=endpoint )
                    #, 'name' : ...
                    , 'positionref' : GDML.ReferenceType(ref=position.get_name())
                    , 'rotationref' : GDML.ReferenceType(ref=rotation.get_name())
                }
        worldVol.add_physvol( GDML.SinglePlacementType( **placementDict ) )
    structure = GDML.structure()
    structure.add_volume(worldVol)
    # - create the GDS object for output document
    gdmlRoot = GDML.gdml()

    gdmlRoot.set_define(defines)
    gdmlRoot.set_materials(materials)
    gdmlRoot.set_solids(solids)
    gdmlRoot.set_structure(structure)
    # - create the default setup
    setup = GDML.setupType( name="Default"
                          , version="1.0"
                          , world=GDML.ReferenceType(ref='World')
                          )
    gdmlRoot.add_setup(setup)
    return gdmlRoot

def export( gdml, index, exportFormat='GDML' ):
    """
    Main export function.
    This procedure will sequentially import submodules related to certain
    output format, expecting them to exist within a Geode package:
        geode.{format}Export._{num}_{name}
    and look for the `read_{name}' function within that will be invoked, in
    order, with the parsed GDML data and index.
    """
    L = logging.getLogger(__name__)
    entitiesList = [
            'definitions',  'materials',
            'solids',       'structure',
            'setup' ]
    sectionsExporters = []
    # Import conversion modules
    for i, entitiesName in enumerate(entitiesList):
        moduleStr = 'geode.{format_}Export._{sectNum}_{sectName}'.format( format_=exportFormat
                , sectNum='%02d'%(1+i)
                , sectName=entitiesName
                )
        m = importlib.import_module(moduleStr)
        f = getattr( m, 'read_' + entitiesName )
        assert(f)
        sectionsExporters.append( (i, f, moduleStr) )
    for expn, export_f, moduleStr in sectionsExporters:
        if export_f:
            L.debug( 'Invoking %s function of "%s"'%(str(export_f), moduleStr) )
            export_f( gdml, index )
        else:
            L.info('Export of "%s" omitted')
