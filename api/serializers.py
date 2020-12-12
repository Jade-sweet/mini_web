"""序列化类部分"""

from rest_framework import serializers

from api.helpers import ParamsException
from api.re_helper import check_username, check_password, check_tel
from common.models import HouseInfo, User, LoginLog


class LoginLogSerializer(serializers.ModelSerializer):
    """登录信息信息序列化器"""

    class Meta:
        """声明序列化字段"""
        model = LoginLog
        exclude = ('user', )


class HouseInfoSimpleSerializer(serializers.ModelSerializer):
    """简单的房屋信息序列化器"""

    class Meta:
        """声明序列化字段"""
        model = HouseInfo
        fields = ('houseid', 'city', 'county', 'comm_name', 'street',
                  'metro', 'area', 'price', 'house_style')


class HouseInfoDetailSerializer(serializers.ModelSerializer):
    """详细房屋信息序列化"""

    class Meta:
        """声明序列化字段"""
        model = HouseInfo
        exclude = ('house_num', 'user')


class RegisterSerializer(serializers.Serializer):
    """注册验证序列化"""
    username = serializers.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'})
    tel = serializers.CharField(required=True, error_messages={'required': '电话不能为空'})

    def validate(self, attrs):
        """验证方法"""
        username = attrs.get('username')
        password = attrs.get('password')
        tel = attrs.get('tel')
        if not check_username(username):
            raise ParamsException({'code': 40002, 'message': '用户名不符合规范'})
        if not check_password(password):
            raise ParamsException({'code': 40002, 'message': '密码不符合规范'})
        if not check_tel(tel):
            raise ParamsException({'code': 40002, 'message': '手机号不符合规范'})
        if User.objects.filter(tel=tel).exists():
            raise ParamsException({'code': 40002, 'message': '手机号已存在'})
        if User.objects.filter(username=username).exists():
            raise ParamsException({'code': 40002, 'message': '用户名已存在'})
        return attrs


class FindPasswordSerializer(serializers.Serializer):
    """找回密码校验"""
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'})
    tel = serializers.CharField(required=True, error_messages={'required': '电话不能为空'})

    def validate(self, attrs):
        """验证方法"""
        password = attrs.get('password')
        tel = attrs.get('tel')
        if not check_password(password):
            raise ParamsException({'code': 40002, 'message': '密码不符合规范'})
        if not check_tel(tel):
            raise ParamsException({'code': 40002, 'message': '手机号不符合规范'})
        if not User.objects.filter(tel=tel).exists():
            raise ParamsException({'code': 40002, 'message': '手机号尚未注册'})
        return attrs
