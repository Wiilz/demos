from werkzeug.exceptions import HTTPException

from apps import create_app
from apps.libs.error import ApiException
from apps.libs.error_code import ServerError
app = create_app()


# 为了捕捉所有的异常, 我们需要绑定异常的基类, Flask > 1.0
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, ApiException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return ApiException(code=code, msg=msg, error_code=error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        raise e


if __name__ == '__main__':
    app.run(debug=False)
