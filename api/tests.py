import json

import requests
from django.test import TestCase

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'test_app.settings')
django.setup()
from common.models import *

# Create your tests here.


# api模块接口测试
class ApiTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """所有测试开始前要执行的方法"""
        print(f'{cls.__name__}测试开始')

    @classmethod
    def tearDownClass(cls):
        """所有测试结束后执行的代码"""
        print(f'{cls.__name__}测试结束')

    def test_token(self):
        """测试登录"""
        response = self.client.post('/api/token/',
                                    json.dumps({'username': '13568528070', 'password': '123456'}),
                                    content_type="application/json")
        self.assertEqual(200, response.status_code)

