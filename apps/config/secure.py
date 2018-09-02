import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASEDIR + '/flaskapi'
SECRET_KEY = 'guess'
TOKEN_EXPIRATION = 30 * 24 * 3600
