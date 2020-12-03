"""
A toy server. Run snippet for dev:
    $ FLASK_ENV=development FLASK_APP=serve.py flask run -p 5600 --host=172.17.0.2
"""
import logging
import logging.config

logging.config.fileConfig( fname='logging.ini'
                         #, disable_existing_loggers=False
                         )

L = logging.getLogger(__name__)

import os
from flask import Flask, url_for, jsonify, make_response
from geode.flask.views import GeometryAPI, geomlib_item_view
from geode.flask.binding import GeodeForFlask

L.info("Creating new app instance")
app = Flask( __name__
           , static_folder="static"  # XXX, we do not have static really...
           #, template_folder='geomlib/'
           )
#app.config.from_yaml(os.path.join(app.root_path, 'server-config.yaml'))
L.info("App instantiated.")
gdmlLib = GeodeForFlask(app)

setupView = GeometryAPI.as_view('geometry_api')
# Setups/assemblies overview
app.add_url_rule( '/geometry/'
                , defaults={'setupID': None, 'contentType' : None}
                , view_func=setupView, methods=['GET',]
                )
# Setups
app.add_url_rule( '/geometry/<int:setupID>.<string:contentType>'
                #, defaults={'itemID':None, 'bontentType': None}
                , view_func=setupView
                , methods=['GET',]
                )
# Setups, editing
app.add_url_rule( '/geometry/<int:setupID>'
                , view_func=setupView
                , methods=['POST', 'PUT', 'PATCH', 'DELETE']
                )
# Individual items
app.add_url_rule( '/geometry/item/<string:itemID>.<string:contentType>'
                #, defaults={'itemID': None, 'contentType' : None}
                , endpoint='geometry_item'
                , view_func=geomlib_item_view, methods=['GET',]
                )

# Site map
#def has_no_empty_params(rule):
#    defaults = rule.defaults if rule.defaults is not None else ()
#    arguments = rule.arguments if rule.arguments is not None else ()
#    return len(defaults) >= len(arguments)
#
#@app.route('/map')
#def site_map():
#    links=[]
#    for rule in app.url_map.iter_rules():
#        url = url_for(rule.endpoint, **(rule.defaults or {}))
#        links.append((url, rule.endpoint))
#    return make_response(jsonify({'map': links}), 200)
print(app.url_map)
