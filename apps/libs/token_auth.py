from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from apps.models.user import User as UserModel
from apps.libs.error_code import AuthFailed, Forbidden
User = namedtuple('User', ['id', 'scope', 'uid'])
auth = HTTPBasicAuth()


# 请求带有@auth.login_required的视图之后,
# 会请求拥有@auth.verify_password装饰器的函数
@auth.verify_password
def verify_password(account, password):
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
    id = data['id']
    scope = data['scope']
    uid = data['uid']
    # 如果没有这个用户则会自动抛出异常
    user = UserModel.query.filter_by(id=id, uid=uid).first()
    if not user:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    return User(id, scope, uid)
