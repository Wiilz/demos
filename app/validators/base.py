from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # 这里如果出错将直接跑出异常, 视图中将免除了判断并使用ifelse的麻烦
            raise ParameterException(msg=self.errors)
        return self
