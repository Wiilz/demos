from werkzeug.exceptions import HTTPException

from apps.libs.error import ApiException


class Success(ApiException):
    code = 200
    msg = 'success'
    error_code = 0

class DeleteSuccess(Success):
    code = 202
    error_code = -1


class GetListSuccess(Success):
    code = 200
    msg = []
    error_code = 0


# 参数错误
class ParameterException(ApiException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class ServerError(ApiException):
    pass

class NotFound(ApiException):
    code = 404
    msg = 'the resource is not found 0.0 '
    error_code = 1001

class AuthFailed(ApiException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005

class Forbidden(ApiException):
    code = 403
    msg = 'Forbidden, not in the scope'
    error_code = 1004

class DumplicatedGift(ApiException):
    code = 400
    error_code = 2001
    msg = 'current book has already in your gifts'


class MethodNotAllowed(Forbidden):
    msg = 'method not allowed'

