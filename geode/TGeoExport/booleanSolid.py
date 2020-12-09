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

import ROOT

# TODO: multiunion!

def transformation_TMatrix_from( pos, rot ):
    #tpos = ROOT.TGeoRotation()
    #tpos.SetDx( pos.computedComponents[0] )
    #tpos.SetDy( pos.computedComponents[1] )
    #tpos.SetDz( pos.computedComponents[2] )
    trot = ROOT.TGeoRotation()
    trot.RotateX( rot.computedComponents[0] )
    trot.RotateY( rot.computedComponents[1] )
    trot.RotateZ( rot.computedComponents[2] )
    # TODO: check, whether rotation here have to be inverted as in
    # ROOT's parser.
    return ROOT.TGeoCombiTrans( pos.computedComponents[0],
                                pos.computedComponents[1],
                                pos.computedComponents[2],
                                trot )  # trot.Inverse() here?

def get_resolver( qType ):
    def resolver_closure_( n, defines ):
        vec = None
        ref = getattr( n, 'get_' + qType + 'ref' )()
        if not ref is None:
            #vec = dpath.util.get( defines, 'defines/' + qType + 's' )
            vec = defines
            for pTok in ('defines/' + qType + 's').split('/'):
                vec = c[pTok]
        else:
            vec = ROOT.Vector3_t()
            qtty = getattr( n, 'get_' + qType )()
            if not qtty is None:
                vec = qtty.to_root_struct( E, vec )
            else:
                tok = qType
                if 'first' in tok:
                    tok = tok[len('first'):]
                getattr( ROOT, 'extGDML_nullate_' + tok )( vec )
        return vec
    return resolver_closure_

def TGeo_boolean_ctr(E, n, quiet=False, defines={}):
    # Note: inline definitions aren't allowed, so <first/> and <second/> are
    # always references.
    firstOperand = defines.get_solid(  n.get_first().get_ref() )
    secondOperand = defines.get_solid( n.get_second().get_ref() )
    resolvers = map( get_resolver, [     'position',      'rotation',
                                    'firstposition', 'firstrotation'] )
    operandBiases = [m(n, defines) for m in resolvers]
    lmat = transformation_TMatrix_from( operandBiases[0], operandBiases[1] )
    rmat = transformation_TMatrix_from( operandBiases[2], operandBiases[3] )
    className = None
    if 'union' == n.get_tagname():
        #print( 'Using TGeoUnion(left, right, lmat, rmat).' )
        className = 'TGeoUnion'
    elif 'subtraction' == n.get_tagname():
        #print( 'Using TGeoSubtraction(left, right, lmat, rmat).' )
        className = 'TGeoSubtraction'
    elif 'intersection' == n.get_tagname():
        #print( 'Using TGeoIntersection(left, right, lmat, rmat).' )
        className = 'TGeoIntersection'
    obj = getattr( ROOT, className )( firstOperand, secondOperand,
                                      lmat, rmat )
    # Note: solids aren't inherited from TNames and thus have no names
    # from ROOT point of view; one have to utilize TGeoCompositeShape
    # in order to make it considerable by TGeo engine:
    obj = ROOT.TGeoCompositeShape( n.get_name(), obj )
    return obj

