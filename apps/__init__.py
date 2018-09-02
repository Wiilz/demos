from apps.api.v1 import create_blueprint_v1
from apps.app import Flask


def register_v1(app):
    from apps.models.base import db
    with app.app_context():
        db.init_app(app)
        db.create_all()


def create_app():
    app = Flask(__name__)
    # app.config.from_object('apps.config.setting')
    app.config.from_object('apps.config.secure')
    app.register_blueprint(create_blueprint_v1())
    register_v1(app)
    return app
