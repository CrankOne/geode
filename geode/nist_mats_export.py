# -*- coding: utf-8 -*-

"""
A set of functions for handling Geant4 material references.

Geant4 defines a number of isotopes, materials and medias based on the NIST
reference. One can reference this definitions with `materialref' tag in GDML,
but they must be defined explicitly for the export.

To accomplish export to other formats, we assume a two-staged procedure after
the GDML is parsed:

    1. First, all the references are collected from the parsed GDML data with
    function `find_refs(gdml)'
    2. Then the material definitions should be composed and emplaced into the
    to-be-exported GDML data with `inject()` function here.
"""

def find_refs( gdml, lib=None ):
    """
    Recursively traverses parsed GDML data looking for any materialref
    mentioning the name that starts with `G4_' suffix.
    """
    mats = set([])
    # Iterate over volumes, look for `materialref' tag, check
    if not gdml.get_structure(): return mats  # no materials used
    # TODO: <assembly/>
    # TODO: <loop/>
    # TODO: ParameterisationAlgorithm ref
    for vol in gdml.get_structure().get_volume():
        matRefName = vol.get_materialref().get_ref()
        if matRefName.startswith('G4_'):
            mats.add( matRefName )
        # check for <file/>
        if vol.get_physvol():
            for subVol in vol.get_physvol():
                if not subVol.get_file():
                    continue
                assert(lib)
                subModFName = subVol.get_file().get_name()
                raise NotImplementedError('TODO: read and parse GDML file for G4_')
                pass  # TODO: file
    return mats

def inject( gdml, defsList ):
    raise NotImplementedError('NIST materials injection')  # TODO

