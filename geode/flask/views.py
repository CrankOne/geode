"""
An extension module for Flask application.
"""

import logging
import yaml
import copy
import io

from flask import Blueprint \
                , request \
                , current_app \
                , url_for \
                , make_response \
                , jsonify \
                , Response \
                , abort
from flask.views import MethodView as FlaskMethodView
from flask_shelve import get_shelve

from geode.export import build_root_GDML

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

    def post(self, contentType):
        """
        Generates a geometry description. We do not _update_ the setups in any
        sense, so no update by setupID is supported here. For full overwrite,
        use PUT.
        Request body must bear a YAML data (as bytes). This choice was made to
        free C/C++ clients from parsing YAML documents.
        TODO:
            - consider JSON inputs?
            - world volume dimensions?
            - improve error reporting
        """
        L = logging.getLogger(__name__)
        # assert request.data
        try:
            detectors = yaml.safe_load(request.data)
        except Exception as e:
            L.exception(e)
            abort(400, 'Error parsing input YAML document')

        # Return JSON preview if this content type requested
        if contentType == 'json':
           return make_response(jsonify(detectors), 200)

        # assert 'assemblies' in detectors
        gdmlRoot = build_root_GDML( detectors['assemblies'].items()
                              , current_app.extensions['geode_gdml'].lib
                              , worldVol={ 'x': 1, 'y':1, 'z':2, 'lunit':'m' }
                              # ^^^ TODO: world size?
                              )
        if contentType == 'gdml':
            strOut = io.StringIO()
            strOut.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE gdml>')
            gdmlRoot.export( strOut, 0, name_='gdml' )
            # TODO: error on non-existing entities
            r = Response(strOut.getvalue(), status=200, mimetype='application/xml')
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        # if contentType == 'root': ...

        abort(400, 'Bad content type requested.')

    def put(self, setupID):
        """
        Creates a geometry description for subsequent use. If setup with the
        same ID exists, overwrites it.
        Returns ???
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
                , defaults={'contentType' : None}
                , view_func=setupView, methods=['GET']
                )
# Setup preview
geodeBlueprint.add_url_rule( '/geometry.<string:contentType>'
                , view_func=setupView, methods=['POST']
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
                , methods=['PUT', 'DELETE']  # 'PATCH'
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

