import yaml
import os
from flask import Flask as FlaskBase \
                , Config as BaseConfig
from geode.view import GeometryAPI

"""
A toy server. Run snippet for dev:
    $ FLASK_ENV=development FLASK_APP=serve.py flask run -p 5600 --host=172.17.0.2
"""

class Config(BaseConfig):
    """
    Flask config enhanced with a `from_yaml` method.
    """
    def from_yaml(self, config_file):
        env = os.environ.get('FLASK_ENV', 'development')
        self['ENVIRONMENT'] = env.lower()
        with open(config_file) as f:
            c = yaml.load(f, Loader=yaml.FullLoader)
        c = c.get(env, c)
        for key in c.keys():
            if key.isupper():
                self[key] = c[key]

class Flask(FlaskBase):
    """
    A Flask's subclass:
        1. Allows configuration from YAML
        2. Provides dependency injection for persistant geometry library
        instance (geode.library.Library).
    """
    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)


app = Flask(__name__)  #, template_folder='geomlib/')
app.config.from_yaml(os.path.join(app.root_path, 'server-config.yaml'))


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

