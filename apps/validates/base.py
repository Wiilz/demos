from flask import request
from wtforms import Form
from apps.libs.error import ApiException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        print(data, args)
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # 这里如果出错将直接跑出异常, 视图中将免除了判断并使用ifelse的麻烦
            raise ApiException(msg=self.errors)
        return self

