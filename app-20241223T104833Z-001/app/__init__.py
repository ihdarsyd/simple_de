from flask import Flask
from jinja2 import TemplateNotFound
from app.home import home_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_blueprint)

    return app