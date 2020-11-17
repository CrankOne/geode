import os
import sys  # XXX

def templates_of( baseDir, criteria ):
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

# any( map( lambda ext: f.endswith(ext), templateExtensions ))
#collect_templates(sys.argv[1])

