import sys
import yaml, json
import logging
from geode.library import Library as GDMLLibrary
import geode.GDMLParser.v3_1_6.classes as GDML  # TODO: ARG

L = logging.getLogger(__name__)

# Read the YAML definitions
with open('specs/detectors.yaml') as f:  # TODO: ARG
    detectors = yaml.load(f, Loader=yaml.FullLoader)

# Print the parsed geometry definitions
#sys.stdout.write(json.dumps(detectors, indent=2))

# Read the geometry library
lib = GDMLLibrary()
lib.import_fs_subtree('specs/geomlib')  # TODO: ARG

#print('Geometry library read. Available assemblies:')
#for k in lib.items.keys():
#    print('  %s'%('/'.join(k)))
sys.stdout.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE gdml>
""")

# NOTE: below, this is for unrestrained!

# Build the setup object from YAML definitions
solids = GDML.solids()
defines = GDML.defineType()
# - create world volume (TODO: take dimensions from a config)
solidWorld = GDML.box( name="solidWorld", x=5, y=1, z=20, lunit='m' )
solids.add_Solid(solidWorld)
worldVol = GDML.VolumeType( name="World"
                          , materialref=GDML.ReferenceType(ref='G4_AIR')
                          , solidref=GDML.ReferenceType(ref=solidWorld.get_name())
                          )
# - iterate over enumerated entries, emplacing the definitions into structure
# as <file/> instances with certain placements
for k, cfgPs in detectors['assemblies'].items():
    if 'geometry' not in cfgPs:
        L.error('The assembly "%s" does not request any geometry. Skip.'%k)
        continue
    geoPath = tuple(cfgPs['geometry'].split('/'))
    if geoPath not in lib.items:
        L.error('No geometry "%s" referenced by "%s" assembly. Skip.'%(
            cfgPs['geometry'], k))
        continue
    # TODO: create named position/rotation for reference
    position = GDML.positionType( name='position_%s'%k
                                , x=cfgPs['placement'][0]
                                , y=cfgPs['placement'][1]
                                , z=cfgPs['placement'][2]
                                , unit=cfgPs['posUnit']
                                , type_='cartesian'
                                )
    rotation = GDML.positionType( name='rotation_%s'%k
                                , x=cfgPs['placement'][3]
                                , y=cfgPs['placement'][4]
                                , z=cfgPs['placement'][5]
                                , unit=cfgPs['rotUnit']
                                , type_='cartesian'
                                )
    defines.add_position( position )
    defines.add_rotation( rotation )
    #print('xxx', lib.items[geoPath])
    # NOTE:
    placementDict = { 'file' : GDML.FileReferenceType( name=lib.items[geoPath]['file'] )
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
#gdmlRoot.set_materials(materials)
gdmlRoot.set_solids(solids)
gdmlRoot.set_structure(structure)
# - create the default setup
setup = GDML.setupType( name="Default"
                      , version="1.0"
                      , world=GDML.ReferenceType(ref='World')
                      )
gdmlRoot.add_setup(setup)

# xxx, print
gdmlRoot.export( sys.stdout, 0, name_='gdml' )

