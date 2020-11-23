# -*- coding: utf8 -*-
# Copyright (c) 2016 Renat R. Dusaev <crank@qcrypt.org>
# Author: Renat R. Dusaev <crank@qcrypt.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
from extGDML.constructorsMapping import auto_CSG_ctr
from extGDML.root.booleanSolid import TGeo_boolean_ctr
from extGDML.root.polyhedra import pgon_ctr
from math import pi as Pi

"""
This module defines adaptation methods constructing ROOT CSG objects from
python objects supplied by auto-generated parser.

Since only few native Geant4 CSG primitives can be directly supported by
ROOT, most of the methods here are manually coded.
"""


def _choose_eltu_ctr( n, defines=None ):
    dPhi = defines.E.convert_units( n.get_deltaphi(), fromUnit=n.get_aunit(),
                                                      toUnit='rad' )
    if 0. == defines.E.evaluate( n.get_startphi() ) \
    and 1e-9 > abs(2*Pi - dPhi ):
        return 'ROOT.TGeoTube'
    else:
        return 'ROOT.TGeoTubeSeg'

gCSGConstructorsDict = {
    'box'       : auto_CSG_ctr( 'ROOT.TGeoBBox',
                        '@name?',
                        '@x:length[cm]={_}/2',
                        '@y:length[cm]={_}/2',
                        '@z:length[cm]={_}/2' ),
    # TODO: cone                : TGeoCone / TGeoConeSeg
    # TODO: ellipsoid           : <none>, see https://github.com/dawehner/root/blob/master/geom/gdml/src/TGDMLParse.cxx#L1660
    'tube'      : auto_CSG_ctr( _choose_eltu_ctr, {
                        #    TGeoTube(Double_t rmin, Double_t rmax, Double_t dz)
                        'ROOT.TGeoTube' : [
                                '@name?',
                                '@rmin:length[cm]',
                                '@rmax:length[cm]',
                                '@z:length[cm]={_}/2'
                            ],
                        # TGeoTubeSeg(Double_t rmin, Double_t rmax, Double_t dz, Double_t phi1, Double_t phi2)
                        'ROOT.TGeoTubeSeg' : [
                                '@name?',
                                '@rmin:length[cm]',
                                '@rmax:length[cm]',
                                '@z:length[cm]={_}/2',
                                '@startphi:angle[degree]',
                                '@deltaphi:angle[degree]={startphi}+{deltaphi}'
                            ]
                        } ),
    'eltube'    : auto_CSG_ctr( 'ROOT.TGeoEltu',
                        # TGeoEltu(Double_t a, Double_t b, Double_t dz) 
                        '@name?',
                        '@dx:length[cm]',
                        '@dy:length[cm]',
                        '@dz:length[cm]'
                        ),
    # TODO: Elliptical cone     : <none>
    'orb'       :  auto_CSG_ctr( 'ROOT.TGeoSphere', # name, rmin, rmax, theta1, theta2, phi1, phi2
                        '@name?',
                        '!=0',
                        '@r:length[cm]={_}',
                        '!:angle[degree]=0',   '!:angle[degree]=pi*rad',
                        '!:angle[degree]=0',   '!:angle[degree]=2*pi*rad' ),
    # TODO: Paraboloid          : TGeoParaboloid
    # TODO: Parallelipiped      : <none>
    # TODO: Polycone            : TGeoPCon
    # TODO: polyhedra           : ?
    'polyhedra' : pgon_ctr,
    # TODO: Generic polycone    : TGeoPCon (?)
    # TODO: Polyhedron          : TGeoPgon
    # TODO: Generic Polyhedron  : TGeoPgon (?)
    # TODO: Sphere              : TGeoSphere
    # TODO: Torus Segment       : TGeoTorus (fully?)
    # TODO: Trapezoid           : <none>
    # TODO: General Trapezoid   : <none>
    # TODO: genericPolyhedra    : ?
    # TODO: Hyperbolic Tube     : <none> (TGeoHype?)
    # TODO: Cut Tube            : ?
    # TODO: Tube Segment        : ?
    # TODO: Twisted Box         : ? (TGeoArb8)
    # TODO: Twisted Trapezoid   : ? (TGeoArb8)
    # TODO: Twisted	General	Trapezoid : ? (TGeoArb8)
    # TODO: Twisted	Tube Segment : ?
    # TODO: Extruded Solid      : ?
    # TODO: Arbitrary Trapezoid : ?
    # TODO: Tessellated	solid   : ?
    # TODO: Tetrahedron         : ?

    # TODO: Loop over solids
    # TODO: Boolean operations: union, multiunion, intersection
    'BooleanSolidType' : TGeo_boolean_ctr,
    #'subtraction' : auto_CSG_ctr( 'TGeoSubtraction',
    #                    '@first/ref:TGeoShape',     # left
    #                    '@second/ref:TGeoShape',    # right
    #                    '!:=NULL',
    #                    '@'  # well, we need a transformation mitrix here (TODO)
    #                    )
    # TODO: Scaled solids

    # TODO: A LOT of paremeterised volumes...
}


