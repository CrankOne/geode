# -*- coding: utf8 -*-

from ._01_definitions import vector_quantity_to_root_struct, \
                                 rotation_from_v3, \
                                 position_from_v3, \
                                 scale_from_v3
import logging

sentinel = object()

def _get_or_resolve_closures_generator( attrName,
                                        inline_translator,
                                        overrideGetterTag=None ):
    """
    Generates a function getting or sesolving certain ROOT object.
    Implies that element `gdmlNode' contains either element named
    `attrName', either element named `attrName' + 'ref'. E.g.:
    '<position/>' or '<positionref/>', '<rotation/>' or '<rotationref/>',
    etc.
    If reference is given he generated function will perform look-up in
    the index object (parameter `I').
    If lement is embedded (inline) the translator function will be invoked to
    perform construction of specific anonymous ROOT object.
    """
    def _get_or_resolve_closure( gdmlNode, I, default=sentinel ):
        # First, try to acquire inline-defined object:
        gdmlObj = getattr( gdmlNode, 'get_' + attrName )()
        if gdmlObj is None:
            # Acquizition of inline failed, try to resolve reference:
            elRef = getattr( gdmlNode, 'get_' + attrName + 'ref' )()
            if elRef is None:
                if default is sentinel:
                    raise KeyError( 'Neither element "%s", nor reference to it '
                        'were found in element "%s"'%(attrName, str(gdmlNode)) )
                else:
                    return default
            return I.get( overrideGetterTag if overrideGetterTag else attrName,
                          elRef.get_ref() )
        else:
            # Inline acquizition succeeded, invoke translator:
            return inline_translator( gdmlObj, I.E, qTag=attrName )
    return _get_or_resolve_closure

def _v3_root_struct_constructor( gdmlObject, E, qTag=None ):
    import ROOT
    L = logging.getLogger(__name__)
    destStr = ROOT.Vector3_t()
    vector_quantity_to_root_struct( gdmlObject, E, destStr )
    rootStruct=None
    if 'position' == qTag:
        rootStruct = position_from_v3( destStr )
    elif 'rotation' == qTag:
        rootStruct = rotation_from_v3( destStr )
        L.debug( 'rotation ctr invoked: %s -> %s'%(destStr, rootStruct) )
    elif 'scale' == qTag:
        rootStruct = scale_from_v3( destStr )
    else:
        raise ValueError("Automatic conversion for tag \"%s\" unimplemented." \
            %str(destStr.qType) )
    return (destStr, rootStruct)

get_or_resolve_position = \
    _get_or_resolve_closures_generator( 'position',
                                        _v3_root_struct_constructor )
get_or_resolve_rotation = \
    _get_or_resolve_closures_generator( 'rotation',
                                        _v3_root_struct_constructor )

get_or_resolve_direction = \
    _get_or_resolve_closures_generator( 'direction',
                                        _v3_root_struct_constructor,
                                        overrideGetterTag='position' )

get_or_resolve_direction = \
    _get_or_resolve_closures_generator( 'scale',
                                        _v3_root_struct_constructor )

