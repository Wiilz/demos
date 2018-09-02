from flask import request
from werkzeug.exceptions import HTTPException

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import  Success
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.redprint import Redprint
api = Redprint('client')

@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        # 如果还有其他的注册类型, 主要增加相应的键值对即可
    }
    # 此时form.type.data的值是由, ClientTypeEnum(value.data)得来, 结果行如<C.USER_EMAIL: 100>,  而上方字典的键, 正是这样的
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
