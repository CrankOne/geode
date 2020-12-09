"""
Error-checking wrapper over Python binding for CLHEP evaluator imported from
a standalone package
"""

import CLHEPEvaluator
import logging
from functools import wraps

class CLHEPEvaluatorError(RuntimeError):
    """
    An exception thrown on CLHEP evaluator error.
    """
    def __init__(self, code, message):
        super(CLHEPEvaluatorError, self).__init__(message)
        self._code = code

    @property
    def code(self):
        return self._code

def check_status(method):
    """
    Auxiliary method called by ordinary methods.
    Retrieves the last operation status and raises exception if it is
    not ok.
    """
    def _args2str(*args, **kwargs):
        return ', '.join( [str(v) for v in args]
                        + ['%s="%s"'%(str(k), str(v)) for k, v in kwargs.items()])
    @wraps(method)
    def _impl(self, *args, **kwargs):
        L = logging.getLogger(__name__)
        try:
            ret = method(self, *args, **kwargs)
        except Exception as e:
            L.error("A Python level exception was thrown by the binding code;"
                    " method: %s, args=(%s), position=%d"%(
                        method.__name__,
                        _args2str(*args, **kwargs),
                        self.error_position()
                        ))
            raise
        status = self.status()
        if CLHEPEvaluator.OK == status: return ret  # ok
        # Warnings
        if CLHEPEvaluator.WARNING_EXISTING_VARIABLE == status:
            L.warning("Redefinition of existing variable (%s); method: %s, args=(%s), position=%d"%(
                self.error_name(),
                method.__name__, _args2str(*args, **kwargs) ),
                self.error_position()
                )
            return ret
        if CLHEPEvaluator.WARNING_EXISTING_FUNCTION == status:
            L.warning("Redefinition of existing function (%s); method: %s, args=(%s), position=%d"%(
                self.error_name(),
                method.__name__, _args2str(*args, **kwargs) ),
                self.error_position()
                )
            return ret
        if CLHEPEvaluator.WARNING_BLANK_STRING == status:
            L.warning("Empty input string (%s); method: %s, args=(%s), position=%d"%(
                self.error_name(),
                method.__name__, _args2str(*args, **kwargs) ),
                self.error_position()
                )
            return ret
        # Errors
        msg = self.error_name()
        msg += "; method: %s, args=(%s), position=%d"%(
                method.__name__, _args2str(*args, **kwargs), self.error_position() )
        raise CLHEPEvaluatorError( status, msg )
    return _impl

class Evaluator(CLHEPEvaluator.Evaluator):
    """
    Error-checking wrapper for Python bindings over the CLHEP evaluator class.
    """

    def __init__(self):
        super(Evaluator, self).__init__()

    @check_status
    def evaluate(self, expression):
        if not isinstance(expression, str):
            expression = str(expression)
        return super(Evaluator, self).evaluate(expression)

    @check_status
    def set_variable(self, name, expr):
        return super(Evaluator, self).set_variable(name, expr)

    @check_status
    def find_variable(self, name):
        return super(Evaluator, self).find_variable(name)

    @check_status
    def find_function(self, name, nargs):
        return super(Evaluator, self).find_function(name, nargs)

    @check_status
    def remove_variable(self, name):
        return super(Evaluator, self).remove_variable(name)

    @check_status
    def remove_function(self, name, nargs):
        return super(Evaluator, self).remove_function(name, nargs)

    @check_status
    def clear(self):
        return super(Evaluator, self).remove_variable()

    @check_status
    def set_std_math(self):
        return super(Evaluator, self).set_std_math()

    @check_status
    def set_system_of_units(self, **kwargs):
        return super(Evaluator, self).set_system_of_units(**kwargs)

    @check_status
    def convert_units(self, val, fromUnit='1', toUnit='1'):
        s = '({val})*({fromUnit})/({toUnit})'.format(**{
            'val' : val, 'fromUnit' : fromUnit, 'toUnit' : toUnit})
        return self.evaluate( s )

    def eval_int(self, expr):
        res = self.evaluate( expr )
        if not res.is_integer():
            raise ValueError( '"%s" evaluated not to whole number (%e) while integer '
                'is expected.'%( expr, res ) )
        return int(res)

