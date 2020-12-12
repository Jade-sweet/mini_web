import hashlib
import io
import json
import os
import random
import uuid

import qiniu
import qrcode
from PIL import Image
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import caches
from django.db.models import Q
from django.db.transaction import atomic
from pymysql import IntegrityError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from api.re_helper import ACCESSKEYID, ACCESSSECRET, SIGN_NAME, SMS_CODE
from common.consts import QINIU_BUCKET_NAME, AUTH
from common.models import User, SpiderHistory
from test_app import app, settings


@app.task
def spider_app(userid, city, area, comm):
    """启动爬虫"""
    # 根目录
    SPIDER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(SPIDER_DIR)
    os.system('scrapy crawl spider -a user_id=%d -a city=%s -a area=%s' % (userid, city, area))
    return None


def get_ip_address(request):
    """获得请求的IP地址"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ip or request.META['REMOTE_ADDR']


def get_dev_info(request):
    """获取硬件信息"""
    dev = ''
    try:
        dev = request.environ.get("HTTP_USER_AGENT")
    except Exception as e:
        pass
    finally:
        return dev


def to_md5_hex(data):
    """生成MD5摘要"""
    if type(data) != bytes:
        if type(data) == str:
            data = data.encode()
        elif type(data) == io.BytesIO:
            data = data.getvalue()
        else:
            data = bytes(data)
    return hashlib.md5(data).hexdigest()


def upload_file_to_qiniu(file_path, filename):
    """将文件上传到七牛云存储"""
    token = AUTH.upload_token(QINIU_BUCKET_NAME, filename)
    return qiniu.put_file(token, filename, file_path)


def upload_stream_to_qiniu(file_stream, filename, size):
    """将数据流上传到七牛云存储"""
    token = AUTH.upload_token(QINIU_BUCKET_NAME, filename)
    return qiniu.put_stream(token, filename, file_stream, None, size)


def upload_image_to_local(user, files):
    """将用户图片存到本地"""
    # 准备文件名
    file_name = f'{uuid.uuid4()}{os.path.splitext(files.name)[1]}'
    # 确定保存路径
    image_path = os.path.join(settings.UPLOADFILES_DIRS, file_name)

    # 如果用户之前尚未修改过图片
    if user.user_image != 'none.png':
        # 删除原有的图片，存入新的图片
        old_path = user.user_image
        old_image_path = os.path.join(settings.UPLOADFILES_DIRS, old_path)
        os.remove(old_image_path)
    user.user_image = file_name
    user.save()
    # 存入图片
    content = files.read()
    with open(image_path, 'wb') as f:
        f.write(content)
    return file_name



def make_thumbnail(image_file, path, size, keep=True):
    """生成缩略图"""
    image = Image.open(image_file)
    origin_width, origin_height = image.size
    if keep:
        target_width, target_height = size
        w_rate, h_rate = target_width / origin_width, target_height / origin_height
        rate = w_rate if w_rate < h_rate else h_rate
        width, height = int(origin_width * rate), int(origin_height * rate)
    else:
        width, height = size
    image.thumbnail((width, height))
    image.save(path)


def gen_qrcode(data):
    """生成二维码"""
    image = qrcode.make(data)
    buffer = io.BytesIO()
    image.save(buffer)
    return buffer.getvalue()


class DefaultResponse(Response):
    """定义返回JSON数据的响应类"""

    def __init__(self, code=100000, message='操作成功',
                 data=None, status=None, template_name=None,
                 headers=None, exception=False, content_type=None):
        _data = {'code': code, 'message': message}
        if data:
            _data.update(data)
        super().__init__(_data, status, template_name,
                         headers, exception, content_type)


class LoginAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # 取得令牌
        token = request.META.get('HTTP_TOKEN')
        if token:
            # 鉴定是否合法
            userid = caches['default'].get(token)
            user = User.objects.filter(userid=userid).first()
            if user:
                user.is_authenticated = True
                return user, token
        raise AuthenticationFailed({'code': 401, 'message': '尚未登录或登录超时 请重新登录'})


# 发送短信
@app.task
def aliyu_message(nums, tel):
    #
    client = AcsClient(ACCESSKEYID, ACCESSSECRET, 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', tel)
    request.add_query_param('SignName', SIGN_NAME)
    request.add_query_param('TemplateCode', SMS_CODE)
    request.add_query_param('TemplateParam', "{\"code\":%s}" % nums)
    response = client.do_action(request)
    if json.loads(str(response, encoding='utf-8'))['Code'] == 'OK':
        # 将验证码存入redis, 存入有效期5分钟
        caches['default'].set(f'{tel}_time', nums, timeout=300)

