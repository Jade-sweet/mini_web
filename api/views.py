import re
import uuid

from django.core.cache import caches
from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


# 只提供查询单个和查询多个的方法
from urllib3.util import current_time

from api.helpers import CustomPagePagination, HouseInfoFilter, LOGIN_ERROR, PASSWORD_ERROR, \
    LOGIN_SUCCESS, REGISTER_ERROR, REGISTER_SUCCESS, PASSWORD_ILLEGAL, OLD_PASSWORD_ERROR, PASSWORD_SUCCESS, \
    FIND_PASSWORD_SUCCESS, CACHE_ERROR, LOGOUT_SUCCESS, BeforPath, DefaultImagePath, GET_IMAGE_SUCCESS, MAX_PHOTO_SIZE, \
    UPLOAD_IMAGE_FAIL, UPLOAD_IMAGE_SUCCESS, GET_LOG_SUCCESS, INFO_EXISTS, INFO_SUCCESS
from api.re_helper import check_password, check_username, check_tel
from api.serializers import HouseInfoSimpleSerializer, HouseInfoDetailSerializer, RegisterSerializer, \
    FindPasswordSerializer, LoginLogSerializer
from common.helpers import DefaultResponse, to_md5_hex, get_ip_address, LoginAuthentication, get_dev_info, \
    upload_image_to_local
from common.models import HouseInfo, User, LoginLog


@api_view(('POST', ))
def user_login(request):
    """用户登录"""
    # 取得数据
    username = request.data.get('username')
    password = request.data.get('password')
    # 序列化
    if check_username(username) or check_tel(username) and check_password(password):
        password = to_md5_hex(password)
        q = Q(username=username, password=password) | \
            Q(tel=username, password=password)
        user = User.objects.filter(q).first()
        if user:
            user_token = uuid.uuid4()
            caches['default'].set(user_token, user.userid, 3600*24)
            loginlog = LoginLog()
            loginlog.user = user.userid
            loginlog.logdate = current_time
            # 获取设备的IP地址
            loginlog.ipaddr = get_ip_address(request)
            # 获取登录设备硬件信息
            loginlog.devcode = get_dev_info(request)
            loginlog.save()
            image_path = BeforPath + user.user_image
            return DefaultResponse(*LOGIN_SUCCESS, {'results': {'token': user_token, 'user_image_path': image_path}})
        else:
            return DefaultResponse(*PASSWORD_ERROR)
    else:
        return DefaultResponse(*LOGIN_ERROR)


@api_view(('POST', ))
def user_register(request):
    """用户注册"""
    data = request.data
    print(data)
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    # 获取验证码
    tel = serializer.validated_data['tel']
    tel_code = request.data.get('tel_code')
    if tel_code == caches['default'].get(f'{tel}_time'):
        # 验证码失效
        caches['default'].delete_pattern(f'{tel}_time')
        with atomic():
            user = User()
            user.password = to_md5_hex(serializer.validated_data['password'])
            user.tel = serializer.validated_data['tel']
            user.username = serializer.validated_data['username']
            user.user_image = DefaultImagePath
            user.save()
        return DefaultResponse(*REGISTER_SUCCESS)
    return DefaultResponse(*CACHE_ERROR)


@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def user_logout(request):
    """用户退出登录"""
    token = request.META.get('HTTP_TOKEN')
    caches['default'].delete_pattern(token)
    return DefaultResponse(*LOGOUT_SUCCESS)


@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def get_image(request):
    """用户获取当前头像"""
    token = request.META.get('HTTP_TOKEN')
    user = User.objects.filter(userid=caches['default'].get(token)).only('user_image').first()
    # 拼接路径
    image_path = BeforPath + user.user_image
    return DefaultResponse(*GET_IMAGE_SUCCESS, {'results': image_path})


@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def get_user_info(request):
    """用户获取当前个人信息"""
    token = request.META.get('HTTP_TOKEN')
    user = User.objects.filter(userid=caches['default'].get(token)).only('user_image').first()
    # 拼接路径
    image_path = BeforPath + user.user_image
    # 用户名
    username = user.username
    # 手机号
    tel = user.tel
    return DefaultResponse(*GET_IMAGE_SUCCESS,
                           {'results':
                                {'image_path': image_path, 'username': username, 'tel': tel}})


@api_view(('POST', ))
@authentication_classes((LoginAuthentication,))
def new_image(request):
    """用户更新当前头像"""
    token = request.META.get('HTTP_TOKEN')
    # 取得图片数据流
    file = request.FILES.get('image_files')
    if file and len(file) <= MAX_PHOTO_SIZE:
        user = User.objects.filter(userid=caches['default'].get(token)).only('user_image').first()
        # 自定义的图片处理函数
        file_path = upload_image_to_local(user, file)
        # 拼接地址
        image_path = BeforPath + file_path
        return DefaultResponse(*UPLOAD_IMAGE_SUCCESS, {'results': image_path})
    return DefaultResponse(*UPLOAD_IMAGE_FAIL)


@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def get_log(request):
    """用户获取登录记录"""
    token = request.META.get('HTTP_TOKEN')
    user = User.objects.filter(userid=caches['default'].get(token)).only('user_image').first()
    logs = LoginLog.objects.filter(user=user.userid).order_by('-logdate').all()
    # 以下注释内容为分页显示
    # # 创建一个分页对象，此对象为自己编写的分页类，或者也可以是默认的
    # paginator = CustomPagePagination()
    # # 传入已有的记录
    # logs = paginator.paginate_queryset(logs, request)
    serializer = LoginLogSerializer(data=logs, many=True)
    # 注意这儿不要写 raise_exception=True
    serializer.is_valid()
    datas = serializer.data
    # datas = paginator.get_paginated_response(serializer.data).data
    return DefaultResponse(*GET_LOG_SUCCESS, {'results':datas})


@api_view(('POST',))
@authentication_classes((LoginAuthentication,))
def change_password(request):
    """修改密码"""
    password = request.data.get('password')
    password1 = request.data.get('password1')
    # 从请求头取得用户口令
    token = request.META.get('HTTP_TOKEN')
    if check_password(password) and check_password(password1):
        user = User.objects.filter(userid=caches['default'].get(token)).first()
        if user.password == to_md5_hex(password):
            user.password = to_md5_hex(password1)
            user.save()
            return DefaultResponse(*PASSWORD_SUCCESS)
        return DefaultResponse(*OLD_PASSWORD_ERROR)
    return DefaultResponse(*PASSWORD_ILLEGAL)


@api_view(('POST',))
@authentication_classes((LoginAuthentication,))
def change_user_tel(request):
    """修改密码"""
    username = request.data.get('username')
    tel = request.data.get('tel')
    # 从请求头取得用户口令
    token = request.META.get('HTTP_TOKEN')
    # 取得该用户
    user = User.objects.filter(userid=caches['default'].get(token)).first()
    # 判断用户名是否存在
    user1 = User.objects.filter(username=username).only('username').first()
    user2 = User.objects.filter(tel=tel).only('tel').first()
    print(user)
    print(user1)
    print(user2)
    if (user1 and user1 != user) or (user2 and user2 != user):
        return DefaultResponse(*INFO_EXISTS)
    tel_code = request.data.get('tel_code')
    if tel_code == caches['default'].get(f'{tel}_time'):
        # 验证码失效
        caches['default'].delete_pattern(f'{tel}_time')
        with atomic():
            user.username = username
            user.tel = tel
            user.save()
        return DefaultResponse(*INFO_SUCCESS)
    return DefaultResponse(*CACHE_ERROR)


@api_view(('POST', ))
def find_password(request):
    """找回密码"""
    data = request.data
    serialzer = FindPasswordSerializer(data=data)
    serialzer.is_valid(raise_exception=True)
    # 获取验证码
    tel_code = data.get('tel_code')
    tel = serialzer.validated_data['tel']
    if tel_code == caches['default'].get(f'{tel}_time'):
        # 验证码失效
        caches['default'].delete_pattern(f'{tel}_time')
        # 找到对应用户
        user = User.objects.filter(tel=serialzer.validated_data['tel']).first()
        user.password = to_md5_hex(serialzer.validated_data['password'])
        user.save()
        return DefaultResponse(*FIND_PASSWORD_SUCCESS)
    return DefaultResponse(*CACHE_ERROR)


class HouseInfoViewSet(ReadOnlyModelViewSet):
    """查看房源"""
    # 取得全部对象
    queryset = HouseInfo.objects.all()
    # 指定筛选类和排序类
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定自己写的筛选类
    filterset_class = HouseInfoFilter
    # 默认的排序字段
    ordering = '-price'
    # 可选的排序字段
    ordering_fields = ('price', 'area', 'metro')
    # 序列化类
    serializer_class = HouseInfoSimpleSerializer
    # 分页
    pagination_class = CustomPagePagination
    # 验证登录
    # authentication_classes = (LoginAuthentication, )

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset\
                .only('houseid', 'city', 'county', 'street', 'comm_name', 'metro', 'price', 'area', 'house_style')
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HouseInfoDetailSerializer
        return HouseInfoSimpleSerializer

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return DefaultResponse(*(10003, '请求成功'), result.data)

    def retrieve(self, request, *args, **kwargs):
        result = super().retrieve(request, *args, **kwargs)
        return Response({'code': 1004, 'message': '请求成功', 'results': [result.data]})