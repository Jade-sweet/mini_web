# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SpiderHistory(models.Model):
    spiderid = models.AutoField(primary_key=True)
    city = models.CharField(max_length=20)
    comm = models.CharField(max_length=20)
    recorddate = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tb_spider_history'
        unique_together = (('city', 'comm'),)


class HouseInfo(models.Model):
    """房屋信息"""
    houseid = models.AutoField(primary_key=True, verbose_name='房屋id')
    house_num = models.CharField(max_length=50, unique=True, verbose_name='唯一编号')
    city = models.CharField(max_length=32, verbose_name='市')
    county = models.CharField(max_length=32, verbose_name='县')
    street = models.CharField(max_length=32, verbose_name='街道')
    comm_name = models.CharField(max_length=32, verbose_name='小区名')
    price = models.IntegerField(default=0, verbose_name='价格')
    longitude = models.CharField(max_length=32, verbose_name='经度')
    latitude = models.CharField(max_length=32, verbose_name='纬度')
    area = models.IntegerField(default=0, verbose_name='面积')
    orientation = models.CharField(max_length=10, verbose_name='朝向')
    priceunit = models.CharField(max_length=10, null=False, verbose_name='价格单位')
    check_in_time = models.CharField(max_length=20, verbose_name='入住时间')
    floor = models.CharField(max_length=20, verbose_name='所在楼层')
    lift = models.CharField(max_length=10, verbose_name='电梯')
    car_station = models.CharField(max_length=10, verbose_name='车位')
    water = models.CharField(max_length=10, verbose_name='用水类型')
    power = models.CharField(max_length=10, verbose_name='用电类型')
    gas = models.CharField(max_length=4, verbose_name='煤气')
    lease_term = models.CharField(max_length=20, verbose_name='租房时间')
    rent_share = models.CharField(max_length=20, verbose_name='租房方式')
    house_style = models.CharField(max_length=20, verbose_name='房屋类型')
    furniture = models.CharField(max_length=128, verbose_name='家具')
    fur_num = models.IntegerField(default=0, verbose_name='家具')
    metro = models.IntegerField(default=0, verbose_name='地铁距离')
    detail_link = models.CharField(max_length=128, verbose_name='详情链接')
    user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, db_column='userid', verbose_name='所属用户')
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tb_house_info'


class HouseType(models.Model):
    """房屋类型"""
    typeid = models.IntegerField(primary_key=True, verbose_name='类型id')
    name = models.CharField(max_length=255, verbose_name='房屋类型')
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tb_house_type'


class LoginLog(models.Model):
    """登录日志"""
    # 日志ID
    logid = models.BigAutoField(primary_key=True)
    # 登录的用户
    # user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, db_column='userid')
    user = models.IntegerField(db_column='userid')
    # 登录的IP地址
    ipaddr = models.CharField(max_length=255)
    # 登录的日期
    logdate = models.DateTimeField(auto_now_add=True)
    # 登录的设备编码
    devcode = models.CharField(max_length=255, default='')
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tb_login_log'


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20, null=False)
    password = models.CharField(max_length=32, null=False)
    tel = models.CharField(unique=True, max_length=20, null=False)
    user_image = models.CharField(max_length=128, null=False)
    regdate = models.DateTimeField(auto_now_add=True)
    lastvisit = models.DateTimeField(null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'tb_user'

