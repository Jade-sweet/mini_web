# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# house_id, city,quyu,jiedao,community_name, price, longitude, latitude, area, orientation,check_in_time,floor,lift,car_station,water,power, gas, lease_term,rent_share, house_style,supporting_facilities,metro,detail_link,user_id


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 1房子id
    house_id = scrapy.Field()
    house_num = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    street = scrapy.Field()
    comm_name = scrapy.Field()
    price = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    area = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    priceunit = scrapy.Field()
    check_in_time = scrapy.Field()
    floor = scrapy.Field()
    car_station = scrapy.Field()
    water = scrapy.Field()
    power = scrapy.Field()
    gas = scrapy.Field()
    lift = scrapy.Field()
    # 租期
    lease_term = scrapy.Field()
    rent_share = scrapy.Field()
    house_style = scrapy.Field()
    furniture = scrapy.Field()
    fur_num = scrapy.Field()
    metro = scrapy.Field()
    # 详细网址
    detail_link = scrapy.Field()
    # 用户id
    userid = scrapy.Field()