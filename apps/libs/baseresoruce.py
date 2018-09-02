from flask.views import MethodView

from apps.libs.error_code import MethodNotAllowed

class BaseResource(MethodView):
    def get(self):
        raise MethodNotAllowed()

    def put(self):
        raise MethodNotAllowed()

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()

    def option(self):
        raise MethodNotAllowed()

    def patch(self):
        raise MethodNotAllowed()