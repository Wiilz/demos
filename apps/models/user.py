from flask import request, current_app
from sqlalchemy import Integer, Column, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.models.base import Base, db
from apps.libs.error_code import AuthFailed


class User(Base):
    id = Column(db.Integer, primary_key=True)
    nick_name = Column(String(20), default='未知')
    uid = db.Column(db.String(64))
    auth = Column(SmallInteger, default=1)  # 权限标志
    _password = Column(String(128))

    def keys(self):
        return ['id', 'nick_name']

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        result = check_password_hash(self._password, raw)
        if not result:
            raise AuthFailed()

    @classmethod
    def users_count(cls):
        """用户总数"""
        return cls.query.count()

    def generic_token(self):
        """生成token"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        scope = 'AdminScope' if self.auth == 2 else 'UserScope'
        code = s.dumps({
            'id': self.id,
            'scope': scope,
            'uid': self.uid
        })
        return code.decode('ascii')

