import uuid

from apps import create_app
from apps.models.base import db
from apps.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nick_name = 'Super'
        user.password = '123456'
        user.auth = 2
        user.uid = str(uuid.uuid4())
        db.session.add(user)
