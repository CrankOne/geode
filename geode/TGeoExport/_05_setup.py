# -*- coding: utf8 -*-

"""
File describes routines for conversion the GDML structure hierarchy definition
into corresponding ROOT TGeo instances.

Shouldn't be used as a separate module. Import extGDML.root.bindings instead.
"""

import ROOT
import logging

def dbg_dump_nodes( el, level=1 ):
    L = logging.getLogger(__name__)
    L.info( ' '*4*level, '- GetName() ->', el.GetName() )
    if( not el.GetShape() ):
        raise RuntimeError('Shapeless volume!')
    L.info( ' '*4*(level), '  ... GetShape() -> ', el.GetShape() )
    L.info( ' '*4*(level), '  ... IsAssembly() -> ', el.GetShape().IsAssembly() )
    if el.GetNodes():
        L.info( ' '*4*(level), '  ...', el.GetNodes().GetSize(), 'child nodes' )
        for i in range( 0, el.GetNodes().GetSize() ):
            n = el.GetNode(i)
            if not n:
                L.info( ' '*4*(level), '  ... #', i, 'NULL node' )
                continue
            if n.GetVolume():
                subVol = n.GetVolume()
            else:
                L.info( ' '*4*(level), '  ... #', i, '<no volume>' )
            if n.GetNodes():
                dbg_dump_nodes( subVol, level=(level+1) )
    else:
        L.info( ' '*4*level, '    - No child nodes.' )


def read_setup( gdml, I,
                quiet=False, setupName='Default',
                auxResults={}, *args, **kwargs ):
    setupDescription = None
    namedSetups = filter( lambda el: setupName == el.get_name(),
                          gdml.get_setup() )
    if len( namedSetups ) > 1:
        raise NotImplementedError( 'Selection by setup name "%s" leads to '
                'disambiguation; versions indexing are not supported yet.'% \
                setupName )
    elif not namedSetups:
        raise KeyError( "Has not setup named \"%s\"."%setupName )
    else:
        setupDescription = namedSetups[0]
    auxResults['topVolume'] = I.get_volume( setupDescription.get_world().get_ref() )

    if kwargs.get('finalizeGeometry', False):
        if not quiet:
            L.info( 'Closing geometry...' )
        # XXX: dev
        if False:
            for k, obj in I.D['volumes'].iteritems():
                #if 'World' == k: continue  # since will always trigger
                L.info( 'Checking volume %s:'%k )
                dbg_dump_nodes(obj)
                #L.info( '    - IsAssembly() ->', obj.IsAssembly() )
                #obj.PrintNodes()
        ROOT.gGeoManager.SetTopVolume( auxResults['topVolume'] )
        ROOT.gGeoManager.CloseGeometry()
        if ROOT.gFile:
            ROOT.gGeoManager.Write()
    return auxResults['topVolume']

