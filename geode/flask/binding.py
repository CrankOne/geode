"""
Application extension.
"""

from flask import current_app, _app_ctx_stack
import logging
from geode.library import Library

class GeodeForFlask(object):
    """
    Flask extension for Geode. Usage:

        from geode.flask_geode import GeodeForFlask
        gdmlLib = GeodeForFlask(app)

    The `GDML_LIBRARY' config variable shall denote the path for the geometry
    library subtree.
    """
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)

    def read_lib(self):
        L = logging.getLogger(__name__)
        L.debug('Loading geometry library subtree'
                ' from "%s"'%current_app.config['GDML_LIBRARY'])
        l = Library()
        l.import_fs_subtree(current_app.config['GDML_LIBRARY'])
        L.debug("Geometry library subtree imported.")
        return l

    def init_setups(self):
        L = logging.getLogger(__name__)
        L.debug('Creating '
                ' from "%s"'%current_app.config['GDML_LIBRARY'])
        l = Library()
        l.import_fs_subtree(current_app.config['GDML_LIBRARY'])
        L.debug("Geometry library subtree imported.")
        return db

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

    @property
    def setups(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'geode_setups'):
                ctx.geode_setups = self.init_setups()
            return ctx.geode_setups

