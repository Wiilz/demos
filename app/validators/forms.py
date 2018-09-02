from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空'), Length(min=5, max=32)])
    secret = StringField()  # 密码不一定是必须的, 因为需要支持各种登录方式
    # 客户端的类型
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            # value表示用户传来的type数据, value.data表示用户传来的数据的值
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise ValidationError(message='客户端错误')
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(Email(message='输入合法的邮箱'))
    # 邮箱注册需要一个密码
    secret = StringField(Regexp(r'^\w{6,22}$', message='请输入6-22位合法字符'))
    # 邮箱注册需要一个用户名
    nickname = StringField(validators=[DataRequired(message='昵称不可以为空')])

    # 是否已经注册过
    def validate_account(self, value):
        user = User.query.filter_by(email=value.data).first()
        if user:
            raise ValidationError(message='重复的邮箱')

    def validate_nickname(self, value):
        user = User.query.filter_by(nickname=value.data).first()
        if user:
            raise ValidationError(message='重复的用户名')


class BookSearchForm(BaseForm):
    q = StringField(validators=[DataRequired()])
