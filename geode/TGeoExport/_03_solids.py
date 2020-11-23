# -*- coding: utf8 -*-

"""
File describes routines for conversion the GDML solids definitions into
corresponding ROOT structures.

Shouldn't be used as a separate module. Import extGDML.root.bindings instead.
"""

from extGDML.root.CSG import gCSGConstructorsDict
import logging
import ROOT

def read_solids( gdml, I,
                 quiet=False, *args, **kwargs ):
    """
    This function is designed to work with <solids/> section of GDML document.
    Parsed entities here steer the creation of ROOT TGeo entities (CSG
    primitives, boolean operations and replicas). Created instances are then
    indexed by name in `defs' dictionary at 'solids/'.
    """
    from extGDML.root.loop import treat_loop_element
    L = logging.getLogger(__name__)
    for solid in gdml.get_solids().Solid:
        className = solid.__class__.__name__
        ctr = gCSGConstructorsDict.get( className, None )
        if ctr is None:
            L.warning( 'CSG solid class "%s" is not yet '
                          'supported. Omitting construction --- possible '
                          'errors ahead possible.'%className )
            continue
        solidTObj = ctr( I.E, solid, quiet=quiet, defines=I )
        I.set_solid( solidTObj, name=solid.get_name() )

