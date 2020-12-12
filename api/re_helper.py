import re
from functools import partial

USERNAME = re.compile(r'^[a-zA-Z\u4e00-\u9fa5]{2,16}$')
PASSWORD = re.compile(r'^[a-zA-Z0-9\.]{6,16}$')
TEL = re.compile(r'^1[3-9][0-9]{9}$')

ACCESSKEYID = 'LTAI4Fsv3QHxempTBHWkwR5E'
ACCESSSECRET = 'ZUOfgoQ5ENgkaZsvuMOJFPiPSUpZag'
SMS_CODE = 'SMS_183245960'
SIGN_NAME = '丝雨记账'


def check_with_pattern(pattern, value, *, hint=False):
    """使用正则表达式检查输入的值"""
    if hint:
        return '' if pattern.match(value) else f'{value} is invalid'
    else:
        return pattern.match(value)


check_username = partial(check_with_pattern, USERNAME)
check_password = partial(check_with_pattern, PASSWORD)
check_tel = partial(check_with_pattern, TEL)
