from enum import Enum


class ClientTypeEnum(Enum):
    # 邮箱
    USER_EMAIL = 100
    # 手机
    USER_MOBILE = 101
    # 微信小小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201
