"""
An extension module for Flask application. Defines a view blueprint that
implements RESTful API.

Disclaimer: the REST (and HAL) are still the set of recommendations. I.e. one
may find contradictive prescriptions of what PUT/POST/PATCH methods have to do.
Moreover we are obliged to consider a small RPC usacease, so the interpretation
of methods semantics may differ from canonical ones:

    - GET: retrieve a collection or item
    - POST: process the request's body (and create new item), return the
        processing result (RPC use case here). ID must not be specified.
    - PUT: insert or replace item (without processing), ID must be specified
    - DELETE: remove item

Practically this means that client can submit a YAML document as raw text
in body, the server will process it (with or without creating entry in
persistent storage) and return the result in a response body. Contrary, the
PUT implementation will expect JSON/GDML data in a request body and desired
ID for an item must be provided with a request data.
"""

import logging
import yaml
import copy
import hashlib

from flask import Blueprint \
                , request \
                , current_app \
                , url_for \
                , make_response \
                , jsonify \
                , Response \
                , abort
from flask.views import MethodView as FlaskMethodView

from .models import GeometriesStorageInterface as Geometries
from geode.export import build_root_GDML, gdml2str

geodeBlueprint = Blueprint( 'geode'
                          , __name__
                          #, template_folder='templates'
                          )

def qpar_as_bool(pn, default):
    return request.args.get(pn, default).lower() in {'true', 'yes', '1'}

def item_js(itemID, item):
    r = { k:str(v) for k,v in item.items() if k not in {'data', 'file'} }
    r['id'] = itemID
    r['_links'] = { 'self' : url_for('geode.geometry_item', itemID=','.join(itemID), contentType='json' ) }
    return r

def item_resolver( itemEntry  # geomlib item entry (file, warnings, data)
                 , itemKey  # an item's key within a library
                 , itemName  # item key, as provided in client's config
                 , itemConfig  # item config, as provided in client's config
                 ):
    """
    Returns a URI for GDML module based on current routing rules (a "name"
    attribute of `<file/>' tag). Since this resolver is designed to be used
    as generator for XercesC-compatible parser, the `_external` is used
    to produce a fully-qualified URL rather then relative path.

    TODO: take into account user's override? (via querystring?)
    """
    return url_for( 'geode.geometry_item'
                  , itemID=','.join(itemKey)
                  , contentType='gdml'
                  , _external=True )

def generate_document(detectors, contentType):
    # assert 'assemblies' in detectors
    gdmlRoot = build_root_GDML( detectors['assemblies'].items()
                          , current_app.extensions['geode_gdml'].lib
                          , worldVol={ 'x': 1, 'y':1, 'z':2, 'lunit':'m' }
                          # ^^^ TODO: world size?
                          , file_resolver=item_resolver
                          )
    if contentType == 'gdml':
        # TODO: error on non-existing entities
        r = Response(gdml2str(gdmlRoot), status=200, mimetype='application/xml')
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    if contentType == 'root':
        raise NotImplementedError('Export to TGeo fromat.')  # TODO
    abort(400, 'Bad content type requested.')

#
# Views

def geomlib_item_view( itemID, contentType='json', item=None, lib=None ):
    """
    A view function for the geometry library item(s).
    """
    response = {}
    response['_links'] = { 'self' : url_for( 'geode.geometry_item'
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
    if 'gdml' == contentType:
        r = Response(gdml2str(item['data']), status=200, mimetype='application/xml')
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    if 'root' == contentType:
        raise NotImplementedError('Export to TGeo fromat.')  # TODO
    abort(400, 'Bad content type requested.')


class GeometryAPI(FlaskMethodView):
    """
    An API for managing setup descriptions. Depending on requested content type
    may respond with JSON or GDML. In latter case, the GDML templating engine
    will be exploited.

    TODO:
        - GET/DELETE methods must support multiple semicolon-delimeted IDs
    """

    def post(self, contentType):
        """
        Creates a geometry description ("setup").

        Request body must bear a YAML data (as bytes). This choice was made to
        free C/C++ clients from parsing YAML documents. A query string
        parameter "noCreate" will prevent setup creation.

        We do not _update_ the setups in any sense, so no update by geometryID
        is supported here. For full overwrite, use PUT. Note that submitting the
        same YAML content without "noCreate" or, equivalently, "noCreate=false",
        will cause creation of new setup each time.

        TODO:
            - consider JSON inputs?
            - world volume dimensions?
            - improve error reporting

        Returns
            200 - OK; returned if "noCreate" is true. Depending on content type
                response brings a result of YAML parsing (.json) or a root GDML
                document (.gdml)
            201 - Created; returned once new setup entry is created. Returned
                body contains a link to the newly created setup entry.
            400 - Client brought no data, YAML parsing failed or
                bad/unsupported content type requested.
        """
        L = logging.getLogger(__name__)
        create = not qpar_as_bool("noCreate", False)
        if not request.data: abort(400, "Request didn't bring any data.")
        # assert request.data
        try:
            detectors = yaml.safe_load(request.data)
        except Exception as e:
            L.exception(e)
            abort(400, 'Error parsing input YAML document')

        gmtID = None
        if create:
            gmtID = Geometries().create(detectors)

        # Return JSON preview if this content type requested
        if contentType == 'json':
            if gmtID is None:
                # RPC case, return parsed setup JSON
                return make_response(jsonify(detectors), 200)
            else:
                # Return link on newly-created object
                return make_response(jsonify({
                        "geometryID":gmtID,
                        "_links": {
                            "self": url_for( 'geode.geometry_api'
                                           , geometryID=gmtID
                                           , contentType=contentType)
                        }
                    }), 201)
        # TODO: rest of the view method shall return a GDML. However, for a
        # normal (setup creation) case, the GDML must be appended with setup ID
        if create: raise NotImplementedError('Returning a GDML/TGeo for persistent setup in GDML response.')
        return generate_document(detectors, contentType)

    def get(self, geometryID=None, contentType=None):
        """
        Reads setup by id(s).
            200 -- ok
            404 -- setup not found
        TODO:
            - support for multiple semicolon-delimeted IDs.
        """
        gs = Geometries()
        if geometryID is None:  # browse the available geometries
            if contentType and contentType != 'json':
                raise NotImplementedError(  # TODO?
                        'Unable to list geometries in format, other than JSON.')
            response = {
                    '_links' : { 'self' : url_for( 'geode.geometry_api'
                                                 , geometryID=geometryID
                                                 , contentType=contentType) },
                    '_embedded': { 'geometry': [] }
                }
            for gmtID in gs.list():
                response['_embedded']['geometry'].append({
                        'id' : geometryID,
                        '_links': {
                            'self': url_for( 'geode.geometry_api'
                                           , geometryID=gmtID
                                           , contentType=contentType ),
                            'gdml': url_for( 'geode.geometry_api'
                                           , geometryID=gmtID
                                           , contentType=gdml ),
                        }
                    })
            return make_response(jsonify(response), 200)
        else:  # produce the document for specific certain geometryID(s)
            detectors = gs.get(geometryID)
            return generate_document(detectors, contentType)

    #def put(self):
    #    """
    #    Replaces existing setup entirely.
    #        200 -- ok
    #        204 -- no content
    #        404 -- not found
    #    """
    #    pass

    #def patch(self):
    #    """
    #    Modifies part of existing setup.
    #        200 -- ok
    #        204 -- no content
    #        404 -- not found
    #    """
    #    pass

    #def delete(self):
    #    """
    #    Wipes the setup description
    #        200 -- ok
    #        404 -- setup not found
    #    """
    #    pass

    #def put(self, geometryID):
    #    """
    #    Creates a geometry description for subsequent use. If setup with the
    #    same ID exists, overwrites it.
    #        201 -- created; on new item created
    #        303 -- see other (?); on item
    #    """
    #    db = get_shelve('c')
    #    if db.get(geometryID, None) is None:
    #        db[geometryID] = request.body
    #    pass

#
# Setting up views

setupView = GeometryAPI.as_view('geometry_api')
# Geometries overview
geodeBlueprint.add_url_rule( '/geometry/'
                , defaults={'contentType' : None}
                , view_func=setupView, methods=['GET']
                )
# Geometry preview
geodeBlueprint.add_url_rule( '/geometry.<string:contentType>'
                , view_func=setupView, methods=['POST']
                )
# Setups
geodeBlueprint.add_url_rule( '/geometry/<int:geometryID>.<string:contentType>'
                #, defaults={'itemID':None, 'bontentType': None}
                , view_func=setupView
                , methods=['GET',]
                )
# Setups, editing
geodeBlueprint.add_url_rule( '/geometry/<int:geometryID>'
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

