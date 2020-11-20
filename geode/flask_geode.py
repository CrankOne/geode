"""
An extension module for Flask application.
"""

from flask import current_app, _app_ctx_stack
from geode.library import Library

class GeodeForFlask(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)

    def read_lib(self):
        l = Library()
        l.import_fs_subtree(current_app.config['GDML_LIBRARY'])
        return l

    def init_app(self, app):
        app.config.setdefault('GDML_LIBRARY', '../geomlib')
        app.extensions['geode_gdml'] = self

    @property
    def lib(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'geode_gdml'):
                ctx.geode_gdml = self.read_lib()
            return ctx.geode_gdml