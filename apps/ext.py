from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter as _Limiter
from flask_limiter.util import get_remote_address
from apps.libs.error import ApiException
from flask_limiter.errors import RateLimitExceeded


class Limiter(_Limiter):

    def __evaluate_limits(self, endpoint, limits):
        try:
            super(Limiter, self).__evaluate_limits(endpoint, limits)
        except RateLimitExceeded:
            raise ApiException(msg='访问速度过快, you\'re to fast', code=439, error_code=999)

from flask_migrate import Migrate
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/second", "100/day"],
)
db = SQLAlchemy()
migrate = Migrate(db=db)

def create_ext(app):
    limiter.init_app(app)
    migrate.init_app(app) 
    db.init_app(app) 
