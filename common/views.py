import os
import random
import re
import threading
from urllib.parse import quote

from django.core.cache import caches
from django.db.models import Q
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.


# 启动爬虫的代码，需要
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from api.helpers import ParamsException
from api.re_helper import check_tel
from common.city_helper import get_county_helper, pinyin, get_street_helper
from common.citys_helper import CITY_DICT
from common.helpers import spider_app, DefaultResponse, LoginAuthentication, aliyu_message
from common.models import SpiderHistory, User, HouseInfo


# 返回爬虫页
from test_app.settings import CELERY_STATUS


def start_celery(queue):
    """启动celery"""
    # 根目录
    SPIDER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(SPIDER_DIR)
    os.system('celery -A test_app worker -Q %s -l debug -P gevent' % queue)


@api_view(('GET', ))
def index(request):
    # 从Redis获取一个状态，表示是否已经启动了Celery
    celery_status = caches['default'].get('celery_status')
    if celery_status:
        caches['default'].set('celery_status', 'running', 3600*24*30)
    else:
        print('进入')
        # 创建线程来启动celery
        caches['default'].set('celery_status', 'running', 3600*24*30)
        # CELERY_STATUS = True
        QUEUE1 = threading.Thread(target=start_celery, args=('spider_queue',))
        QUEUE2 = threading.Thread(target=start_celery, args=('tel_code_queue',))
        QUEUE1.start()
        QUEUE2.start()
    print('执行')
    return redirect('/static/html/index.html')


# 根据市取得区
@api_view(('GET', ))
# @authentication_classes((LoginAuthentication,))
def get_county(request):
    """动态获取地区"""
    city = request.query_params.get('city', '成都市')
    print(city)
    city = CITY_DICT[city]
    url = 'https://%s.lianjia.com/zufang/rs/' % city
    content = get_county_helper(url)
    # return JsonResponse(content, safe=False)
    return DefaultResponse(*(10002, '请求成功'), {'results': content})


# 动态获取街道
@api_view(('GET', ))
# @authentication_classes((LoginAuthentication,))
def get_street(request):
    """动态获取街道"""
    city = request.query_params.get('city', '成都市')
    city = CITY_DICT[city]
    county = request.query_params.get('county', '十陵')
    # 将区域转为拼音
    county = 'gaoxin7' if county == '高新' else pinyin(county)
    url = 'https://%s.lianjia.com/zufang/%s' % (city, county)
    content = get_street_helper(url)
    # return JsonResponse(content, safe=False)
    return DefaultResponse(*(10002, '请求成功'), {'results': content})

# 爬虫页顶端的提示，图片信息
@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def spider_info(request):
    results = ['/static/images/1.jpg',
               '/static/images/2.jpg',
               '/static/images/3.jpg',
               '/static/images/4.jpg']
    return DefaultResponse(*(10002, '请求成功'), {'results': results})


# 登录页顶端的提示，图片信息
@api_view(('GET', ))
def login_img(request):
    results = ['/static/images/log1.jpg',
               '/static/images/log2.jpg',
               '/static/images/log3.jpg']
    return DefaultResponse(*(10002, '请求成功'), {'results': results})


# 启动爬虫程序
@api_view(('GET', ))
@authentication_classes((LoginAuthentication,))
def spider_start(request):
    userid = 1
    # 搜索城市、地区等，为爬虫做准备
    city = request.query_params.get('city', '成都市')
    comm = request.query_params.get('comm', '十陵')
    print(comm)
    city = CITY_DICT[city]
    # 寻找数据库是否该区域已经爬取过
    if not SpiderHistory.objects.filter(Q(city=city) & Q(comm=comm)).exists():
        print('新增')
        with atomic():
            spi = SpiderHistory()
            spi.city = city
            spi.comm = comm
            spi.save()
        # 搜索地区/小区
        area = quote(comm)
        spider_app.apply_async(
            (userid, city, area, comm),
            # {'tel': tel, 'message': message},
            queue='spider_queue',
            countdown=10,
            # retry_policy={},
            # expires=60,
            # compression='zlib',
        )
    return Response({'code': 10001, 'message': '爬虫启动成功，稍后可查看结果', 'result': {}})


@api_view(('GET',))
def check_login(request):
    """检查登录是否合法"""
    token = request.META.get('HTTP_TOKEN')
    results = 'success' if caches['default'].get(token) else 'false'
    return DefaultResponse(*(200, '请求成功'), {'results': results})


@api_view(('GET',))
def map_info(request):
    """给定市区，返回地图数据"""
    county = request.query_params.get('county')
    if county == '全部':
        houses = HouseInfo.objects.only('comm_name', 'longitude', 'latitude').all()
    else:
        houses = HouseInfo.objects.filter(county=county).only('comm_name', 'longitude', 'latitude').all()
    data1 = []
    data2 = {}
    # 小区名字列表
    comm_list = []
    for item in houses:
        # 找出每个小区对应的房源个数
        comm_list.append(item.comm_name)
        data2[item.comm_name] = [item.longitude, item.latitude]
    if data2:
        local = data2[random.choice(list(data2))]
    else:
        local = [104.043035, 30.653754]
    # 去掉重复房源
    only_comm = set(comm_list)
    for comm_n in only_comm:
        # 组装房屋个数数据
        data1.append({'name': comm_n, 'value': comm_list.count(comm_n)})
    return DefaultResponse(*(200, '请求成功'), {'results': {'data1': data1, 'data2': data2, 'local': local}})


# 调用短信接口
@api_view(('GET', ))
def get_tel_code(request):
    tel = request.query_params.get('tel')
    if not check_tel(tel):
        res = {'code': 40002, 'message': '手机号不合法', 'results': {}}
        raise ParamsException(res)
    # 检查120s内是否发送
    if not caches['default'].get(f'{tel}_limit'):
        # 随机6位数字验证码
        nums = ''.join([str(random.randint(0, 9)) for i in range(6)])
        # 提前缓存，防止双击频繁请求
        caches['default'].set(f'{tel}_limit', nums, timeout=120)
        # 异步发送短信
        aliyu_message.apply_async(
            (nums, tel),
            queue='tel_code_queue',
            countdown=10,
            # retry_policy={},
            # expires=60,
            # compression='zlib',
        )
        return DefaultResponse(*(200, '发送短信成功'))
    return DefaultResponse(*(50002, '发送短信失败，操作过于频繁'))

