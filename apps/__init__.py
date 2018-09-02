from flask import Flask
from apps.ext import create_ext
from apps.views import create_blueprint
from apps.model import Url
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    from apps.model import Url
    CORS(app, supports_credentials=True)
    app.config.from_object('apps.settings')
    create_blueprint(app)
    create_ext(app)
    return app
