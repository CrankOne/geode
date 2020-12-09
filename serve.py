"""
A toy server. Run snippet for dev:
    $ FLASK_ENV=development FLASK_APP=serve.py flask run -p 5600 --host=172.17.0.2
"""
import logging
import logging.config

logging.config.fileConfig( fname='logging.ini'
                         #, disable_existing_loggers=False
                         )

L = logging.getLogger( __name__ )

import os
from flask import Flask, url_for, jsonify, make_response
# extensions
import flask_shelve as shelve


from geode.flask.views import geodeBlueprint
from geode.flask.binding import GeodeForFlask

L.info("Creating new app instance")
app = Flask( __name__
           , static_folder="static"  # XXX, we do not have static really...
           #, template_folder='geomlib/'
           )

app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

app.register_blueprint( geodeBlueprint )
gdmlLib = GeodeForFlask(app)

print(app.url_map)
