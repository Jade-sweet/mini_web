import datetime
from functools import wraps

from django.db.models import Q
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view

from common.helpers import DefaultResponse
from common.models import HouseInfo


def run_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        a = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print(end_time-start_time)
        return a
    return wrapper


@api_view(('GET', ))
def every_county_count(request):
    """各区总套数"""
    data1 = ['锦江', '青羊', '武侯', '高新', '成华', '金牛',
             '天府新区', '双流', '温江', '郫都',
             '龙泉驿', '新都', '彭州', '简阳', '青白江', '都江堰']
    data2 = []
    for item in data1:
        data2.append(HouseInfo.objects.filter(county=item).count())
    return DefaultResponse(*(200, '请求成功'), {'results': {'data1': data1, 'data2': data2}})


@api_view(('GET', ))
def price_county_count(request):
    """各区各价格段总套数"""
    data1 = ['锦江', '青羊', '武侯', '高新', '成华', '金牛',
             '天府新区', '双流', '温江', '郫都',
             '龙泉驿', '新都', '彭州', '简阳', '青白江', '都江堰']
    price_list = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000',
                  '5000-10000']
    price_dict = {}
    for pri in price_list:
        data2 = []
        for item in data1:
            data2.append(HouseInfo.objects.filter(Q(county=item) &
                                                  Q(price__lte=pri.split('-')[1]) &
                                                  Q(price__gte=pri.split('-')[0])).count())
            price_dict[pri] = data2
    return DefaultResponse(*(200, '请求成功'), {'results': {'data2': price_dict}})


@api_view(('GET', ))
def my_test2(request):
    """计算各区的平均价格"""
    data1 = ['锦江', '青羊', '武侯', '高新', '成华', '金牛',
             '天府新区', '双流', '温江', '郫都',
             '龙泉驿', '新都', '彭州', '简阳', '青白江', '都江堰']
    return DefaultResponse()


@api_view(('GET', ))
def my_test3(request):
    """计算各个面积段的租房数量"""
    data1 = ['0-20', '20-50', '50-80', '80-110', '110-140', '140-170', '170-200']
    data2 = []
    for i in data1:
        data2.append(
            {'value': HouseInfo.objects.filter(Q(area__gt=int(i.split('-')[0])) & Q(area__lte=int(i.split('-')[1]))).count(),
            'name': i})
    return DefaultResponse(*(200, '成功'), {'data': data2})




