# -*- coding: utf-8 -*-
import hashlib
import time

import requests
import xmltodict
from flask import Flask, request, abort, redirect, jsonify, Blueprint
from accesstoken import AccessToken
app = Flask(__name__)
message = Blueprint(__name__, 'message')
appid = 'wxa0f8e47c1c5eb934'
appsecret = '6db481ba38324f9318f658df4724b893'


@message.before_request
def prepare():
    """验证消息"""
    args = request.args.to_dict()
    if not args:
        return 'args is missed '
    my_signature = args.get('signature')  # 获取携带的signature参数
    my_timestamp = args.get('timestamp')  # 获取携带的timestamp参数
    my_nonce = args.get('nonce')  # 获取携带的nonce参数
    my_echostr = args.get('echostr')  # 获取携带的echostr参数
    token = 'token111'
    # 进行字典排序
    data = [token, my_timestamp, my_nonce]
    data.sort()
    # 拼接成字符串
    temp = ''.join(data)
    # 进行sha1加密
    mysignature = hashlib.sha1(temp).hexdigest()
    # 加密后的字符串可与signature对比，标识该请求来源于微信
    print('正在验证消息')
    if my_signature != mysignature:
        abort(403)


@message.route('/wechat', methods=['GET', 'POST'])
def test():
    """公众号回复测试"""
    if request.method == 'GET':
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        return my_echostr
    if request.method == 'POST':
        xml_data = request.data
        data = xmltodict.parse(xml_data).get('xml')
        msg_type = data.get('MsgType')
        if msg_type == 'text':
            print('text type message')
            content = data.get('Content')
            resp_data = {
                "xml": {
                    'ToUserName': data.get('FromUserName'),
                    'FromUserName': data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': 'I have receive your message: ' + content
                }
            }
            resp_xml_data = xmltodict.unparse(resp_data)
            return resp_xml_data
        return 'success'


# 第三方登录测试: 文档: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140842
@app.route('/login')
def login_test():
    redirect_uri = 'http://wx.wktadmin.com'
    scope = 'snsapi_userinfo'
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=STATE#wechat_redirect'%(appid, redirect_uri, scope)
    return redirect(url)


@app.route('/')
def index():
    args = request.args.to_dict()
    if not args:
        return redirect('/login')
    code = args.get('code')
    if not code:
        return redirect('/login')
    # 获取用户的accesstoken
    access_token, oppenid = get_access_token(code)
    userinfo = get_user_info(access_token, oppenid)
    return userinfo


def get_access_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appid, appsecret, code)
    json_response = requests.get(url).json()
    access_token = json_response.get('access_token')
    oppenid = json_response.get('openid')
    return access_token, oppenid


def get_user_info(access_token, opponid):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (access_token, opponid)
    json_res = requests.get(url).json()
    return jsonify(json_res)


if __name__ == '__main__':
    app.run(debug=True)
