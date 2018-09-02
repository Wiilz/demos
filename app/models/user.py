from sqlalchemy import Integer, Column, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base, db
from app.libs.error_code import NotFound, AuthFailed


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)  # 权限标志
    _password = Column('password', String(100))


    def keys(self):
        return ('id', 'create_time', 'email', 'nickname', 'status')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, acount, secret):
        """
        注册用户
        """
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = acount
            user.password = secret
            db.session.add(user)

    @classmethod
    def verify(cls, email, password):
        # 比对用户输入的密码是否正确, 返回返回user.id
        user = cls.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}
        
    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

