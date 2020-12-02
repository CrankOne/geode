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
from flask import Flask
from geode.view import GeometryAPI
from geode.flask_geode import GeodeForFlask


L.info("Creating new app instance")
app = Flask(__name__)  #, template_folder='geomlib/')
#app.config.from_yaml(os.path.join(app.root_path, 'server-config.yaml'))
L.info("App instantiated.")
gdmlLib = GeodeForFlask(app)

setupView = GeometryAPI.as_view('geometry_api')
app.add_url_rule( '/geometry/'
                , defaults={'setupID': None, 'contentType': None}
                , view_func=setupView, methods=['GET',]
                )
app.add_url_rule( '/geometry/<int:setupID>.<string:contentType>'
                , view_func=setupView, methods=['GET',]
                )
app.add_url_rule( '/geometry/<int:setupID>'
                , view_func=setupView
                , methods=['POST', 'PUT', 'PATCH', 'DELETE']
                )

