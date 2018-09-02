from flask import jsonify, g

from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.models.base import db
from app.libs.error_code import DeleteSuccess, AuthFailed

# user = Blueprint('user', __name__)
api = Redprint('user')


# 这个装饰器的工作过程是: 当请求访问到带有@auth.login_required的视图时,
# 会请求拥有@auth.verify_password装饰器的函数
@api.route('')
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

@api.route('/create')
@auth.login_required
def create_user():
    return ''


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    print(uid)
    # user = User.query.filter_by(id=uid).first_or_404()
    user = User.query.filter_by(id=uid).first_or_404()

    with db.auto_commit():
        user.delete()  # 逻辑删除, 自定义方法
    return DeleteSuccess()


@api.route('/<int:uid>', methods=['DETELE'])
def super_delete_user(uid):
    """超级管理员删除用户操作"""
    pass


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """超级管理员查询用户"""
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)
