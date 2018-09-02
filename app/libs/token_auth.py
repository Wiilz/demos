from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

User = namedtuple('User', ['uid', 'ac_type', 'scope'])
auth = HTTPBasicAuth()


# 请求带有@auth.login_required的视图之后,
# 会请求拥有@auth.verify_password装饰器的函数
@auth.verify_password
def verify_password(account, password):
    # 为什么这里的参数是account,password而不是token呢?
    # 一个办法: 客户端传递token的时候, 以account的形式传递, 后台便可以接收了.
    # 接下来便是验证token的过程
    userinfo = verify_token(account)
    if not userinfo:
        return False
    else:
        g.user = userinfo
        return True


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature as e:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired as e:
        raise AuthFailed(msg='token is expired', error_code=1002)
    except Exception as e:
        raise e
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
