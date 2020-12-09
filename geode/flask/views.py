"""
An extension module for Flask application.
"""

import logging
import json
import copy
from flask import Blueprint, request, current_app, url_for, make_response, jsonify
from flask.views import MethodView as FlaskMethodView
from flask_shelve import get_shelve

geodeBlueprint = Blueprint( 'geode'
                          , __name__
                          #, template_folder='templates'
                          )

def qpar_as_bool(pn, default):
    return request.args.get(pn, default).lower() in {'true', 'yes', '1'}

def item_js(itemID, item):
    r = { k:str(v) for k,v in item.items() if k not in {'data', 'file'} }
    r['_links'] = { 'self' : url_for('geode.geometry_item', itemID=','.join(itemID), contentType='json' ) }
    return r


def geomlib_item_view( itemID, contentType='json', item=None, lib=None ):
    """
    A view function for the geometry library item(s).
    """
    response = {}
    response['_links'] = { '_self' : url_for( 'geode.geometry_item'
                                            , itemID=itemID
                                            , contentType=contentType ) }
    # browse items, if no itemID provided
    if itemID is None:
        if contentType is not None and 'json' != contentType:
            return make_response(jsonify({'errors': ['Bad content type requested.']}), 400)
        lib = current_app.extensions['geode_gdml'].lib
        response['_embedded'] = { 'item': [] }
        for k, v in lib.items.items():
            response['_embedded']['item'].append(item_js(k, v))
        return make_response( jsonify(response), 200 );
    # for single item access
    if type(itemID) is str:
        itemID = tuple(itemID.split(','))
    if item is None:
        if lib is None:
            lib = current_app.extensions['geode_gdml'].lib
        item = lib.items[itemID]
    if contentType is None or 'json' == contentType:
        return make_response( jsonify(item_js(item)), 200 )
    return item


class GeometryAPI(FlaskMethodView):
    """
    An API for managing setup descriptions. Depending on requested content type
    may respond with JSON or GDML. In latter case, the GDML templating engine
    will be exploited.
    """

    def post(self, setupID):
        """
        Creates new setup
            404 -- ???
            409 -- setup exists
        """
        db = get_shelve('c')
        if db.get(setupID, None) is None:
            db[setupID] = request.body
        pass

    def get(self, setupID=None, contentType=None):
        """
        Reads setup by id(s)
            200 -- ok
            404 -- setup not found
        """
        response = {}
        response['_links'] = { '_self' : url_for( 'geode.geometry_api'
                                                , setupID=setupID
                                                , contentType=contentType) }
        if setupID is None:  # browse the available geometries
            db = get_shelve('r')
            if not len(db):
                response['_embedded'] = { 'item': [] }
            else:
                pass  # TODO
        elif contentType is None or 'json' == contentType:
            pass  # TODO
        return make_response(jsonify(response), 200)
        #print(current_app.extensions['geode_gdml'].lib.items.keys())
        #if not setupID:
        #    pass  # ... TODO: render XML/JSON of the available setups with HATEOAS
        #if contentType and contentType.lower() in {'gdml', 'GDML', 'xml', 'XML'}:
        #    # Options for GDML rendering
        #    restrained = qpar_as_bool('restrained', False)
        #    disableExtensions = qpar_as_bool('disableExtensions', False)
        #    return render_template( 'root.xml'
        #                          , **model.override_query(request.args.lists()))
        #else:
        #    pass  # ... TODO: return JSON describing particular setup
        #pass

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


setupView = GeometryAPI.as_view('geometry_api')
# Setups/assemblies overview
geodeBlueprint.add_url_rule( '/geometry/'
                , defaults={'setupID': None, 'contentType' : None}
                , view_func=setupView, methods=['GET',]
                )
# Setups
geodeBlueprint.add_url_rule( '/geometry/<int:setupID>.<string:contentType>'
                #, defaults={'itemID':None, 'bontentType': None}
                , view_func=setupView
                , methods=['GET',]
                )
# Setups, editing
geodeBlueprint.add_url_rule( '/geometry/<int:setupID>'
                , view_func=setupView
                , methods=['POST', 'PUT', 'PATCH', 'DELETE']
                )

# Items
geodeBlueprint.add_url_rule( '/geometry/item'
                , defaults={'itemID': None, 'contentType' : None}
                , endpoint='geometry_item'
                , view_func=geomlib_item_view, methods=['GET',]
                )
geodeBlueprint.add_url_rule( '/geometry/item/<string:itemID>.<string:contentType>'
                #, defaults={'itemID': None, 'contentType' : None}
                , endpoint='geometry_item'
                , view_func=geomlib_item_view, methods=['GET',]
                )

