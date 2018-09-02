from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from apps.models.user import User
from apps.validators.base import BaseForm


class UserForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='用户名不允许为空'), Length(min=5, max=32)])
    password = StringField(validators=[DataRequired(message='密码不允许为空'), Length(min=5, max=32)])

    def validate_nickname(self, raw):
        users = User.query.filter_by(nick_name=raw.data).first()
        if users:
            raise ValidationError(message='重复的用户名')


class AuthForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='用户名不允许为空'), Length(min=5, max=32)])
    password = StringField(validators=[DataRequired(message='密码不允许为空'), Length(min=5, max=32)])


class ArticleForm(BaseForm):
    title = StringField(validators=[DataRequired(message='标题不允许为空'), Length(min=5, max=32)])
    content = StringField()
