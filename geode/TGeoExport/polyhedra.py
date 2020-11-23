# -*- coding: utf8 -*-
import ROOT
import logging

def pgon_ctr( E, nodeInstance, quiet=False, defines={},
                toLUnit='cm', toAUnit='degree'):
    """
    Polyhedra (polygon) CSG ctr. For non-generic case it can be imagined as
    a sequence of prisms with scalable transversal cross section planes. In
    GDML they're defined as element with variable (>=1) number of cross
    sections.
    """
    L = logging.getLogger(__name__)
    givenLUnit = nodeInstance.get_lunit()
    givenAUnit = nodeInstance.get_aunit()
    ctrArgs = [
            nodeInstance.get_name(),  # name
            E.convert_units( nodeInstance.get_startphi(),
                             fromUnit=givenAUnit,
                             toUnit=toAUnit ), # phi,
            E.convert_units( nodeInstance.get_deltaphi(),
                             fromUnit=givenAUnit,
                             toUnit=toAUnit ), # dphi,
            E.eval_int( nodeInstance.get_numsides() ), # nedges,
            len( nodeInstance.get_zplane() ) # nz
        ]
    L.debug( 'Polyhedra args: %s'%str(ctrArgs) )
    pgon = ROOT.TGeoPgon( *ctrArgs )
    nzPlane = 0
    for zPlaneNode in nodeInstance.get_zplane():
        sectArgs = [
                nzPlane, # snum
                E.convert_units( zPlaneNode.get_z(),
                             fromUnit=givenLUnit,
                             toUnit=toLUnit ), # z
                E.convert_units( zPlaneNode.get_rmin(),
                             fromUnit=givenLUnit,
                             toUnit=toLUnit ), # rmin
                E.convert_units( zPlaneNode.get_rmax(),
                             fromUnit=givenLUnit,
                             toUnit=toLUnit ), # rmax
            ]
        L.debug( '    + Z-Plane: %s'%str(sectArgs) )
        pgon.DefineSection( *sectArgs )
        nzPlane += 1
    return pgon


