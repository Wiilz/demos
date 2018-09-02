import re
from wtforms import StringField
from wtforms.validators import DataRequired
from apps.validates.base import BaseForm


class UrlForm(BaseForm):
    long_url = StringField('长域名', validators=[DataRequired('域名不可以为空')])

