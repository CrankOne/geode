import sys
import yaml, json
import logging
from geode.library import Library as GDMLLibrary
from geode.export import build_root_GDML

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

# NOTE: below, this is for unrestrained!

sys.stdout.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE gdml>
""")
gdmlRoot = build_root_GDML( detectors['assemblies'].items()
                          , lib
                          , worldVol={ 'x': 1, 'y':1, 'z':2, 'lunit':'m' }  )
# xxx, print
gdmlRoot.export( sys.stdout, 0, name_='gdml' )

