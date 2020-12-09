#!/bin/env python
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
from geode.evaluator import Evaluator
from .refResolve import get_or_resolve_position, \
                        get_or_resolve_rotation
#                       get_or_resolve_scale
import logging

def treat_loop_element( I, gdmlLoopNode, callback,
                        context=None ):
    L = logging.getLogger(__name__)
    if type( context ) is str:
        context = [context]

    iteeName = gdmlLoopNode.get_for()
    iteeFrom = gdmlLoopNode.get_from()
    iteeTo   = gdmlLoopNode.get_to()
    iteeStep = gdmlLoopNode.get_step()

    #if not quiet
    L.debug( 'Loop iterating the "%s" from %s to "%s" with step "%s".'%(
            iteeName, (iteeFrom if iteeFrom else '%e'%I.E.evaluate(iteeName)),
            iteeTo, iteeStep ) )

    fullContextStr = '/'.join(context)

    _to_call = callback
    # .get_Solid():      # ref=Solid, unbounded
    # .get_volume():     # VolumeType, once
    # .get_physvol():    # SinglePlacementType, once
    # .get_loop():       # loop type, unbounded
    def _embedded_loop( deeperLoop ):  # TODO: check
        for l in e.get_loop():
            treat_loop_element( I, deeperLoop, callback,
                                context=(context + ['loop']) )
    if gdmlLoopNode.get_loop():  # loop type, unbounded
        _to_call = _embedded_loop

    # Now, iterate:
    if iteeFrom:
        I.E.setVariable( iteeName, iteeFrom )
    # otherwise it iteration will take place from current value
    if not I.E.findVariable( iteeName ):
        raise('Variable \"%s\" is not defined in loop context %s.'%(
                iteeName, fullContextStr ))

    #while I.E.evaluate(iteeName) < I.E.evaluate(iteeTo):
    #    I.E.setVariable( iteeName, '(%s) + (%s)'%(iteeName, iteeStep) )
    #    _target_closure()
    # ^^^ Note: the block above causes recursion error with CLHEP evaluator.
    # It seems that evaluator does not support such a feature.
    # Original Geant4 <loop/> implementation does not involve evaluating
    # a recusive expressions like `a <- a+1' avoiding this problem via
    # literal evaluation, so do we:
    while I.E.evaluate(iteeName) <= I.E.evaluate(iteeTo):
        newVal = I.E.evaluate( '(%s) + (%s)'%(iteeName, iteeStep) )
        I.E.setVariable( iteeName, '%e'%newVal,
                expectedStatus=Evaluator.WARNING_EXISTING_VARIABLE )
        _to_call( gdmlLoopNode )

