# -*- coding: utf-8 -*-
import re
import os
import time
from math import ceil
import jieba
import scrapy
from django.http import request
from lxml import etree
from lianjia.items import *
from lianjia.spiders.proxy_helper import *


DICT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['lianjia.com']
    # 这句话不起作用
    start_urls = ['https://cd.lianjia.com/zufang/pg2rs%E9%BE%99%E6%B3%89%E9%A9%BF/']

    def __init__(self, city=None, user_id=None, area=None, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        # 拼接的url
        self.start_urls = ['https://%s.lianjia.com/zufang/rs%s/' % (city, area)]
        self.user_id = user_id
        self.city = city
        self.area = area
        self.proxies_ip = {'http': 'http://60.185.66.76:3617', 'https': 'https://60.185.66.76:3617'}

    # 取得首页
    def start_requests(self):
        url = self.start_urls
        headers = {
            'Host': '%s.lianjia.com' % self.city,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        url = 'https://' + self.city +'.lianjia.com/zufang/rs' + self.area + '/'
        try:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse_total, dont_filter=False,
                                 meta={'url': url, 'proxies': self.proxies_ip})
        except:
            time.sleep(3)
            self.proxies_ip = get_proxies()
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse_total, dont_filter=False,
                                 meta={'url': url, 'proxies': self.proxies_ip})
        finally:
            print('+'*30)
            print(self.proxies_ip)

    # 计算需要访问多少页
    def parse_total(self, response):
        html_data = response.text
        etree_html = etree.HTML(html_data)
        # 得到隐藏的url页
        url_pages = etree_html.xpath('//div[@id="content"]//div[@class="content__article"]//ul[@style="display:hidden"]//li/a//@href')
        url_pages.append('/zufang/pg1/rs%s/' % self.area)
        for url_page in url_pages:
            headers = {
                'Host': '%s.lianjia.com' % self.city,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            url = 'https://' + self.city +'.lianjia.com' + url_page
            try:
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse, dont_filter=False,
                                     meta={'url': url, 'proxies': self.proxies_ip})
            except:
                time.sleep(3)
                self.proxies_ip = get_proxies()
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse, dont_filter=False,
                                     meta={'url': url, 'proxies': self.proxies_ip})
            finally:
                print('+' * 30)
                print(self.proxies_ip)

    # 解析每个房子的网页信息
    def parse(self, response):
        html_data = response.text
        etree_html = etree.HTML(html_data)
        # 得到所有的住房的url
        all_house_url = etree_html.xpath('//div[@class="content__list"]//div[@class="content__list--item"]/a[@class="content__list--item--aside"]/@href')
        # 遍历得到的url
        for house_url in all_house_url:
            headers = {
                'Host': '%s.lianjia.com' % self.city,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            url = 'https://' + self.city +'.lianjia.com' + house_url
            try:
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.detail_parse,
                                     dont_filter=False, meta={'url': url, 'proxies': self.proxies_ip})
            except:
                time.sleep(3)
                self.proxies_ip = get_proxies()
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.detail_parse,
                                     dont_filter=False, meta={'url': url, 'proxies': self.proxies_ip})
            finally:
                print('+' * 30)
                print(self.proxies_ip)

    def detail_parse(self, response):
        html_data = response.text
        etree_html = etree.HTML(html_data)
        content = etree_html.xpath('//script[@src="https://s1.ljcdn.com/agent-sj-sdk/1.2.0/agent-sj-sdk.js"]/following-sibling::script[1]/text()')

        content = [c.strip() for c in content][0]
        # 小区名字
        comm_name = re.findall(r"g_conf.name = '(.*?)';", content)[0]
        # 租金
        price = re.findall(r"g_conf.rent_price = '(.*?)';", content)[0]
        # 房屋id
        house_id = re.findall(r"g_conf.houseCode = '(.*?)';", content)[0]
        # 经度
        longitude = re.findall(r"longitude: '(.*?)',", content)[0]
        # 维度
        latitude = re.findall(r"latitude: '(.*?)'", content)[0]
        # 房屋面积
        area = etree_html.xpath('//div[@id="info"]/ul[1]/li[2]/text()')[0][3:-1]
        # 朝向
        orientation = etree_html.xpath('//div[@id="info"]/ul[1]/li[3]/text()')[0][3:].strip().split(' ')[0]
        # 入住时间
        check_in_time = etree_html.xpath('//div[@id="info"]/ul[1]/li[6]/text()')[0][3:]
        # 所在楼层
        floor = etree_html.xpath('//div[@id="info"]/ul[1]/li[8]/text()')[0][3:]
        # 电梯
        lift = etree_html.xpath('//div[@id="info"]/ul[1]/li[9]/text()')[0][3:]
        # 车位
        car_station = etree_html.xpath('//div[@id="info"]/ul[1]/li[11]/text()')[0][3:]
        # 用水
        water = etree_html.xpath('//div[@id="info"]/ul[1]/li[12]/text()')[0][3:]
        # 用电
        power = etree_html.xpath('//div[@id="info"]/ul[1]/li[14]/text()')[0][3:]
        # 燃气
        gas = etree_html.xpath('//div[@id="info"]/ul[1]/li[15]/text()')[0][3:]
        # 租期
        lease_term = etree_html.xpath('//div[@id="info"]/ul[2]/li[2]/text()')[0][3:]
        # 合租?
        rent_share = etree_html.xpath('//ul[@class="content__aside__list"]/li[1]/text()')[0]
        # 房型
        house_style = etree_html.xpath('//ul[@class="content__aside__list"]/li[2]/text()')[0][:7]
        # 地区详细
        diqu_info = re.findall(r'租房信息,(.*?)房屋出租', etree_html.xpath('//meta[@name="keywords"]/@content')[0])
        jieba.load_userdict('%s/spiders/dict.txt' % DICT_DIR)
        diqu_info = list(jieba.cut(diqu_info[0]))
        # 城市
        city = diqu_info[0]
        # quyu
        quyu = diqu_info[1]
        # 街道
        jiedao = ''.join(diqu_info[2:])
        # 配套设施
        supporting_facilities = []
        # 自组合配套设施
        for i in range(2, 12):
            s = etree_html.xpath('//ul[@class="content__article__info2"]/li[%d]//text()' % i)[1].strip('\n').strip(' ')
            if 'facility_no' in etree_html.xpath('//ul[@class="content__article__info2"]/li[%d]/@class' % i)[0]:
                continue
            else:
                supporting_facilities.append(s)
        supporting_facilities = ('_'.join(supporting_facilities) if len(supporting_facilities) != 0 else '未知')
        fur_num = 1 if supporting_facilities == '未知' else 0
        # 最近的地铁
        ditie = etree_html.xpath('//div[@class="content__map"]/following-sibling::ul//text()')
        a = [c.strip() for c in ditie]
        test = re.findall(r'[\u4e00-\u9fa5]?([0-9]*?)m',''.join(a))
        metro = test[0] if len(test) > 0 else '暂无数据'
        # house_id, city,quyu,jiedao,community_name, price, longitude, latitude, area, orientation, check_in_time,floor,lift,car_station,water,power, gas, lease_term,rent_share, house_style,supporting_facilities,metro,detail_link,user_id
        if float(price) > 10000 or float(area) > 200 or float(area) < 15 or float(price) < 256:
            pass
        else:
            item = LianjiaItem()
            item['house_num'] = house_id
            item['city'] = city
            item['county'] = quyu
            item['street'] = jiedao
            item['comm_name'] = comm_name
            item['price'] = price
            item['longitude'] = longitude
            item['latitude'] = latitude
            item['area'] = area
            item['orientation'] = orientation
            item['priceunit'] = '元/月'
            item['check_in_time'] = check_in_time
            item['floor'] = floor
            item['lift'] = lift
            item['car_station'] = '未知' if car_station == '暂无数据' else car_station
            item['water'] = '未知' if water == '暂无数据' else water
            item['power'] = '未知' if water == '暂无数据' else power
            item['gas'] = '未知' if gas == '暂无数据' else gas
            item['lease_term'] = '未知' if lease_term == '暂无数据' else lease_term
            item['rent_share'] = rent_share
            item['house_style'] = house_style
            item['furniture'] = supporting_facilities
            item['fur_num'] = fur_num
            item['metro'] = 99999 if metro == '暂无数据' else int(metro)
            item['detail_link'] = response.meta['url']
            item['userid'] = self.user_id

            yield item



