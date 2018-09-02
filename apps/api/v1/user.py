import uuid

from flask import jsonify, g

from apps.libs.baseresoruce import BaseResource
from apps.libs.token_auth import auth
from apps.models.user import User
from apps.models.base import db
from apps.libs.error_code import DeleteSuccess, AuthFailed, Success
from apps.validators.forms import UserForm, AuthForm


class UserResource(BaseResource):
    """
    注册
    """
    def post(self):
        form = UserForm().validate_for_api()
        with db.auto_commit():
            user = User()
            user.nick_name = form.nickname.data
            user.password = form.password.data
            user.uid = str(uuid.uuid4())
            db.session.add(user)
        return Success(msg=dict(user), code=201, error_code=1)


class AuthResource(BaseResource):
    """
    post: 获取token
    delte: 删除token
    """
    def post(self):
        form = AuthForm().validate_for_api()
        user = User.query.filter_by(nick_name=form.nickname.data).first_or_404()
        user.check_password(form.password.data)
        return Success(msg=user.generic_token())

    @auth.login_required
    def delete(self):
        user = User.query.filter_by(id=g.user.id).first_or_404()
        with db.auto_commit():
            user.uid = str(uuid.uuid4())
            db.session.add(user)
        return Success(code=204)



