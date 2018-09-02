from .view import urlbp


def create_blueprint(app):
    app.register_blueprint(urlbp)
