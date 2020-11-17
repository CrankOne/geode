from flask import Blueprint, render_template, request, Response, url_for, make_response
from flask.views import MethodView as FlaskMethodView

def qpar_as_bool(pn, default):
    return request.args.get(pn, default).lower() in {'true', 'yes', '1'}

class GeometryAPI(FlaskMethodView):
    """
    An API for managing setup descriptions. Depending on requested content type
    may respond with JSON or GDML. In latter case, the GDML templating engine
    will be exploited.
    TODO: versioning
    """
    def post(self, setupID):
        """
        Creates new setup
            404 -- ???
            409 -- setup exists
        """
        pass

    def get(self, setupID=None, contentType=None):
        """
        Reads setup by id(s)
            200 -- ok
            404 -- setup not found
        """
        if not setupID:
            pass  # ... TODO: render XML/JSON of the available setups with HATEOAS
        if contentType.lower() in {'gdml', 'GDML', 'xml', 'XML'}:
            # Options for GDML rendering
            restrained = qpar_as_bool('restrained', False)
            disableExtensions = qpar_as_bool('disableExtensions', False)
            return render_template( 'root.xml'
                                  , **model.override_query(request.args.lists()))
        else:
            pass  # ... TODO: return JSON describing particular setup
        pass

    def put(self):
        """
        Replaces existing setup entirely.
            200 -- ok
            204 -- no content
            404 -- not found
        """
        pass

    def patch(self):
        """
        Modifies part of existing setup.
            200 -- ok
            204 -- no content
            404 -- not found
        """
        pass

    def delete(self):
        """
        Wipes the setup description
            200 -- ok
            404 -- setup not found
        """
        pass

