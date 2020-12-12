from django.db.models import Q
from django_filters import filterset
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination

from common.models import HouseInfo

# 默认头像地址
DefaultImagePath = 'none.png'
# 默认的前缀
BeforPath = '/static/images/user_upload/'
# 图片最大的大小
MAX_PHOTO_SIZE = int(2.5 * 1024 * 1024)

LOGIN_ERROR = (20002, '规则错误')
PASSWORD_ERROR = (20003, '密码或用户名错误')
LOGIN_SUCCESS = (20001, '登录成功')

REGISTER_ERROR = (30002, '注册失败')
CACHE_ERROR = (30003, '验证码错误')
REGISTER_SUCCESS = (30001, '注册成功')

OLD_PASSWORD_ERROR = (40003, '原密码错误')
PASSWORD_ILLEGAL = (40002, '密码格式错误')
PASSWORD_SUCCESS = (40001, '修改成功')

FIND_PASSWORD_SUCCESS = (50001, '密码重置成功')

LOGOUT_SUCCESS = (60001, '退出登录成功')

GET_IMAGE_SUCCESS = (70001, '获取头像成功')
UPLOAD_IMAGE_FAIL = (70003, '上传头像失败，尚未选择文件或文件太大')
UPLOAD_IMAGE_SUCCESS = (70002, '上传头像成功')

GET_LOG_SUCCESS = (80001, '获取记录成功')

INFO_EXISTS = (90002, '用户名或手机号已存在')
INFO_SUCCESS = (90001, '修改信息成功')


class CustomPagePagination(PageNumberPagination):
    """自定义页码分页类"""
    page_size_query_param = 'size'
    max_page_size = 50


class HouseInfoFilter(filterset.FilterSet):
    """房屋过滤类"""
    minprice = filterset.NumberFilter(field_name='price', lookup_expr='gte')
    maxprice = filterset.NumberFilter(field_name='price', lookup_expr='lte')
    minarea = filterset.NumberFilter(field_name='area', lookup_expr='gte')
    maxarea = filterset.NumberFilter(field_name='area', lookup_expr='lte')
    minmetro = filterset.NumberFilter(field_name='metro', lookup_expr='gte')
    maxmetro = filterset.NumberFilter(field_name='metro', lookup_expr='lte')
    area = filterset.CharFilter(method='filter_by_area')

    @staticmethod
    def filter_by_area(queryset, name, value):
        return queryset.filter(Q(city__startswith=value) |
                               Q(county__startswith=value) |
                               Q(street__startswith=value) |
                               Q(comm_name__startswith=value) |
                               Q(house_style__startswith=value))

    class Meta:
        model = HouseInfo
        fields = ('minmetro', 'maxmetro', 'minprice', 'maxprice', 'minarea', 'maxarea', 'area')


class ParamsException(APIException):

    def __init__(self, message):

        self.detail = message
