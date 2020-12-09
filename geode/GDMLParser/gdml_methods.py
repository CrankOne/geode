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

#!/usr/bin/env python
# -*- mode: pymode; coding: latin1; -*-

from __future__ import print_function

import sys
import re

#
# You must include the following class definition at the top of
#   your method specification file.
#
class MethodSpec(object):
    def __init__(self, name='', source='', class_names='',
            class_names_compiled=None):
        """MethodSpec -- A specification of a method.
        Member variables:
            name -- The method name
            source -- The source code for the method.  Must be
                indented to fit in a class definition.
            class_names -- A regular expression that must match the
                class names in which the method is to be inserted.
            class_names_compiled -- The compiled class names.
                generateDS.py will do this compile for you.
        """
        self.name = name
        self.source = source
        if class_names is None:
            self.class_names = ('.*', )
        else:
            self.class_names = class_names
        if class_names_compiled is None:
            self.class_names_compiled = re.compile(self.class_names)
        else:
            self.class_names_compiled = class_names_compiled
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_source(self):
        return self.source
    def set_source(self, source):
        self.source = source
    def get_class_names(self):
        return self.class_names
    def set_class_names(self, class_names):
        self.class_names = class_names
        self.class_names_compiled = re.compile(class_names)
    def get_class_names_compiled(self):
        return self.class_names_compiled
    def set_class_names_compiled(self, class_names_compiled):
        self.class_names_compiled = class_names_compiled
    def match_name(self, class_name):
        """Match against the name of the class currently being generated.
        If this method returns True, the method will be inserted in
          the generated class.
        """
        if self.class_names_compiled.search(class_name):
            return True
        else:
            return False
    def get_interpolated_source(self, values_dict):
        """Get the method source code, interpolating values from values_dict
        into it.  The source returned by this method is inserted into
        the generated class.
        """
        print('XXX %s %s'%(str(self.source), str(values_dict)))
        source = self.source % values_dict
        return source
    def show(self):
        print('specification:')
        print('    name: %s'%(self.name, self.source))
        print('    class_names: %s' % (self.class_names, ))
        print('    names pat  : %s' % (self.class_names_compiled.pattern, ))


#
# Provide one or more method specification such as the following.
# Notes:
# - Each generated class contains a class variable _member_data_items.
#   This variable contains a list of instances of class _MemberSpec.
#   See the definition of class _MemberSpec near the top of the
#   generated superclass file and also section "User Methods" in
#   the documentation, as well as the examples below.

METHOD_SPECS = (

MethodSpec(name='get_numerical_value',
    source='''\
    def get_numerical_value(self, E, forceEvaluation=False):
        # (keep units unused, however may come from few descendants line)
        if not hasattr(self, 'evaluatedVal') or forceEvaluation:
            self.evaluatedVal = E.evaluate( self.get_value() )
        return self.evaluatedVal
''',
    class_names=r'^(Variable|Constant)Type$',
    ),

MethodSpec(name='get_numerical_value',
    source='''\
    def get_numerical_value(self, E, forceEvaluation=False):
        """
        Performs calculation of quantity in absolute units using provided
        evaluator instance. Evaluator must have evaluate() method accepting
        string expression.
        The self.measuredVal attribute then will contain numerical value of initilal
        expression in given units (dimensionless value).
        The self.evaluatedVal then will contain numerical value of quantity in
        absolute units (defined by evaluator instance.)
        
        The self.evaluatedVal is a returned value.
        """
        if not hasattr(self, 'evaluatedVal') or forceEvaluation:
            self.measuredVal = E.evaluate( self.get_value() )
            print('XX#1', self.measuredVal, self.get_unit())  # XXX
            self.evaluatedVal = E.evaluate( "({v})*({u})".format( **{ 
                    'v' : self.measuredVal,
                    'u' : self.get_unit() } ) )
        return self.evaluatedVal
''',
    class_names=r'^QuantityType$',
    ),

MethodSpec(name='convert_value_in_units',
    source='''\
    def convert_value_in_units(self, E, units):
        return E.convert_units( self.get_value(), fromUnit=self.get_unit(),
                                                  toUnit=units )
''',
    class_names=r'^QuantityType$',
    ),

#
# GDML evaluation method will perform declaration for constant/variable.
# using provided CLHEP evaluator instance.
#
MethodSpec(name='get_numerical_value',
    source='''\
    def get_numerical_value(self, E, forceEvaluation=False,
                            forceRedefinition=False):
        """
        Performs calculation of value by invokation parental
        get_numerical_value() method and defines named value in evaluator.
        The evaluator must have setVariable
        """
        v = super(self.__class__, self).get_numerical_value( E, forceEvaluation=forceRedefinition)
        if (not E.findVariable(self.get_name()) or forceRedefinition):
            print('var set: %%s <- '%%self.get_name(), v)  # XXX
            E.setVariable( self.get_name(), v )
        return v
''',
    class_names=r'^Identifiable(Variable|Constant|Quantity)Type$',
    ),

#
# For spatial 3-dim quantities (positions and rotations) we need to evalaute
# components.
# Note that, default values provided in <restriction/> tag
MethodSpec(name='get_evaluated_components',
    source='''\
    def get_evaluated_components(self, E):
        return (E.evaluate( self.x ),
                E.evaluate( self.y ),
                E.evaluate( self.z ))
''',
    #class_names=r'^(position|rotation)Type$',
    class_names=r'^QuantityVectorType$',
    ),

MethodSpec(name='get_absolute_components',
    source='''\
    def get_absolute_components(self, E):
        s = "({c})*({u})"
        unit = self.get_unit()
        return (E.evaluate( s.format(**{'c':self.get_x(), 'u':unit}) ),
                E.evaluate( s.format(**{'c':self.get_y(), 'u':unit}) ),
                E.evaluate( s.format(**{'c':self.get_z(), 'u':unit}) ))
''',
    #class_names=r'^(position|rotation)Type$',
    class_names=r'^QuantityVectorType$',
    ),

MethodSpec(name='get_absolute_components',
    source='''\
    def get_absolute_components(self, E):
        s = "({c})*({u})"
        unit = self.get_unit() if self.get_unit() else 1
        return (E.evaluate( s.format(**{'c':self.get_x(), 'u':unit}) ),
                E.evaluate( s.format(**{'c':self.get_y(), 'u':unit}) ),
                E.evaluate( s.format(**{'c':self.get_z(), 'u':unit}) ))
''',
    #class_names=r'^(position|rotation)Type$',
    class_names=r'^scaleType$',
    ),

# TODO: is there another way to return original tag name for
# substitution groups?
MethodSpec(name='get_tagname',
    source='''\
    def get_tagname(self):
        return self.original_tagname_
''',
    class_names=r'^BooleanSolidType$'
    )

)  # METHOD_SPEC

