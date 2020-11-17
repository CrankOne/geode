import os
from .parser.parser_3_1_6 import parse

def files_at( baseDir, criteria ):
    """
    A generator function returning files matching certain criterion from 
    a directory recursively. 
    """
    for root, dirs, files in os.walk(baseDir, followlinks=True):
        relPath = os.path.relpath(root, baseDir)
        for f in files:
            if criteria(f):
                fullPath = os.path.normpath(os.path.join(relPath, f))
                keys = fullPath.split(os.sep)
                yield keys

def import_assemblies( baseDir, gdmlExtensions={'gdml'} ):
    for assemblyFile in files_at(baseDir,
            lambda fn: any( map(lambda ext: fn.endswith(ext), gdmlExtensions) )):
        assembly = parse_GDML( fn )

#import sys  # XXX
# any( map( lambda ext: f.endswith(ext), templateExtensions ))
#collect_templates(sys.argv[1])

