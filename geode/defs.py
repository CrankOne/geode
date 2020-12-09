# -*- coding: utf8 -*-

"""
Definitions index module

In C++ GDML there is a set of definitions associated with each GDML entity.
They are kept mainly by CLHEP evaluator class with its DSL. This module
provides a Python level for the same purpose, providing exporting routines
an access to these definitions with `DefinitionsIndex' class structuring
the definitions within a dictionary with respect to choosen topology.
"""

from geode.evaluator import Evaluator as G4Evaluator
from types import MethodType
from pprint import pformat
import importlib
import logging

# Our routines expects certain form of definition dictionary, so it is
# better to specify generic topology here explicitly. However, the
# dpath.new() function will recursively create sub-dictionaries.
#definedObjects = {
#    'rootFile' : None,
#    'defines' : {
#        'quantities' : {},
#        'positions' : {},
#        'rotations' : {},
#        'matrices' : {}     # TODO
#    },
#    'materials' : {
#        'isotopes' : {},
#        'elements' : {},
#        'materials' : {}
#    },
#    'solids' : {}
#    # ...
#}

gGeant4SystemOfUnits = {
    "meter"     : 1.e+3,
    "kilogram"  : 1./1.60217733e-25,
    "second"    : 1.e+9,
    "ampere"    : 1./1.60217733e-10,
    "kelvin"    : 1.0,
    "mole"      : 1.0,
    "candela"   : 1.0
}

gDefaultTopology = {
     # defines section:
     'quantity' : 'defines/quantities/{name}',
     'position' : 'defines/positions/{name}',
     'rotation' : 'defines/rotations/{name}',
     'scale'    : 'defines/scales/{name}',
     'matrix'   : 'defines/matrices/{name}',
     # materials / media section:
     'isotope'  : 'materials/isotopes/{name}',
     'element'  : 'materials/elements/{name}',
     'material' : 'materials/materials/{name}',
     'medium'   : 'materials/media/{name}',  # note, that this path is used (*)
     # solids
     'solid'    : 'solids/{name}',
     # volumes:
     'volume'   : 'volumes/{name}'
}

def _generate_shortcuts( k ):
    # Getters:
    def _newgetter_closure(self, *args, **kwargs):
        return self.get( k, *args, **kwargs )
    _newgetter_closure.__name__ = 'get_%s'%k
    # Setters
    def _newsetter_closure(self, *args, **kwargs):
        self.set( k, *args, **kwargs )
    _newsetter_closure.__name__ = 'set_%s'%k
    return ( _newgetter_closure, _newsetter_closure )

class DefinitionsIndex(object):
    """
    Object aggregating definitions local to certain GDML file. Implemented as a
    set of wrappers and shortcuts over dictionary of user-defined topology.

    Constants and variables are represented as instances of Definition_t
    C-struct declared by CINT (so, one have to make CINT parse the
    common/structs.C).
    The scalar quantities are stored as instances of ComputedQuantity_t
    struct.
    Rotations, positions or scales 3-dimensional vector quantity are stored
    as instances of Vector3_t struct.

    The CLHEP evaluator instance is a member of this class.

    It is implied that
    for each parsed GDML file one will instantiate new DefinitionsIndex
    instance. It is convinient to store the hierarchically according to GDML
    files with modular topology.
    """
    supportedEntities = (   # Defines section:
                            'quantity', 'position', 'rotation', 'matrix',
                            # Materials section:
                            'isotope',  'element',  'material', 'medium',
                            # Solids section:
                            'solid',
                            # Structure section:
                            'volume'
                        )
    def __init__( self
                , units=gGeant4SystemOfUnits
                , topology=gDefaultTopology
                , suppMaterialsResolver=None
                ):
        self._topology = topology
        self.units = units
        self.E = G4Evaluator()
        self.E.set_system_of_units( **units )
        self.E.set_std_math()
        # definitions dictionary:
        self.D = {}
        # create shortcut methods:
        for k in self.supportedEntities:
            _newgetter_closure, _newsetter_closure = _generate_shortcuts(k)
            setattr( self.__class__,
                _newgetter_closure.__name__,
                _newgetter_closure )
            setattr( self.__class__,
                _newsetter_closure.__name__,
                _newsetter_closure )
        if( suppMaterialsResolver ):
            def _supp_material_getter( self, name, noexcept=False, **kwargs ):
                matInst = self.get('material', name, noexcept=True,
                                    **kwargs)
                if not matInst:
                    importedMat = suppMaterialsResolver(name, self,
                                            noexcept=noexcept, **kwargs)
                    if importedMat:
                        self.set_material( importedMat, name=name,
                                           noexcept=noexcept )
                    else:
                        # causes ordinary exception
                        return self.get('material', name, noexcept=noexcept,
                                        **kwargs)
                    return importedMat
                else:
                    return matInst
            self.get_material = MethodType(_supp_material_getter, self)
        self.subidxs = {}

    def get(self, entityTypeName, name, noexcept=False, level=0, **kwargs):
        L = logging.getLogger(__name__)
        if not entityTypeName in self.supportedEntities:
            raise SystemError( 'Got unsupported entity type identifier '
                               '"%s" for getter.'%entityTypeName )
        path = self._topology[entityTypeName].format(name=name, **kwargs)
        c = self.D
        for pTok in path.split('/'):
            try:
                c = c[pTok]
            except KeyError:
                # xxx: apparently no need in that sophistication --- Geant4 seems
                # to put all the stuff into one dictionary.
                #if self.parentIndex:
                #    return self.parentIndex.get( entityTypeName, name,
                #            noexcept=noexcept, level=(level+1), **kwargs )
                if noexcept:
                    return None
                else:
                    L.error('For key "%s" at token "%s"'%(path, pTok))  # xxx?
                    raise
        return c

    def set(self, entityTypeName, instance, override=False, **kwargs):
        L = logging.getLogger(__name__)
        if not entityTypeName in self.supportedEntities:
            raise SystemError( 'Got unsupported entity type identifier '
                               '"%s" for setter.'%entityTypeName )
        path = self._topology[entityTypeName].format(**kwargs)
        exists = True
        c = self.D
        for pTok in path.split('/'):
            c = c.get(pTok, None)
            if c is None:
                exists = False
                break
        if exists:
            msg = '%s already contains an entity. Overriden (%s).\n'%(path
                        , ('ok' if override else 'warn'))
            if override:
                L.debug(msg)
            else:
                L.warning(msg)
        c = self.D
        for pTok in path.split('/')[:-1]:
            if pTok not in c:
                c[pTok] = {}
            c = c[pTok]
        c[path.split('/')[-1]] = instance

    def __str__(self):
        return pformat( self.D )

    # XXX, need by some of the deprecated ext.GDML TGeo conversion routines
    def get_media_count(self):
        # Hardcoded to topology (*)
        if 'materials' in self.D.keys():
            if 'media' in self.D['materials'].keys():
                return 1 + len( dpath.util.get( self.D, 'materials/media') )
        return 1

    def new_subindex(self, name, *args, **kwargs):
        si = DefinitionsIndex( *args
                             , units=self.units
                             , **kwargs )
        self.subidxs[name] = si
        return si

    def get_subindex( self, name, noexcept=False ):
        if not noexcept:
            return self.subidxs[name]
        else:
            return self.get(name, None)


