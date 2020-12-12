# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from lianjia.items import LianjiaItem


class LianjiaMysqlPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            sql = 'insert into tb_house_info(house_num, city, county, street, comm_name, price, longitude, latitude,' \
                  ' area, orientation, priceunit, check_in_time, floor, lift, car_station, water,' \
                  ' power, gas, lease_term, rent_share, house_style, furniture, fur_num, metro, detail_link, userid)' \
                  'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                  ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                self.cursor.execute(sql, (item['house_num'], item['city'], item['county'],
                                          item['street'], item['comm_name'], item['price'], item['longitude'],
                                          item['latitude'], item['area'], item['orientation'], item['priceunit'],
                                          item['check_in_time'], item['floor'], item['lift'], item['car_station'],
                                          item['water'], item['power'], item['gas'], item['lease_term'],
                                          item['rent_share'], item['house_style'], item['furniture'], item['fur_num'],
                                          item['metro'], item['detail_link'], item['userid']))
            except Exception as e:
                sql2 = "update tb_house_info set price=%s, check_in_time=%s, car_station=%s, water=%s," \
                       " power=%s, gas=%s, lease_term=%s, rent_share=%s, house_style=%s, furniture=%s, fur_num=%s," \
                       " metro=%s" \
                       " where house_num=%s"
                self.cursor.execute(sql2, (
                    item['price'], item['check_in_time'], item['car_station'],
                    item['water'], item['power'], item['gas'], item['lease_term'],
                    item['rent_share'], item['house_style'], item['furniture'], item['fur_num'],
                    item['metro'], item['house_num']))
        else:
            pass
        self.db.commit()
        return item

    def __init__(self, host, username, password, port, database):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'), username=crawler.settings.get('MYSQL_USERNAME'),
                   password=crawler.settings.get('MYSQL_PASSWORD'), database=crawler.settings.get('MYSQL_DATABASE'),
                   port=crawler.settings.get('MYSQL_PORT'))

    # 蜘蛛对象生成的时候调用
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    # 蜘蛛关闭的时候调用
    def close_spider(self, spider):
        self.db.close()
