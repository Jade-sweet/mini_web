# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbHouseInfo(models.Model):
    houseid = models.AutoField(primary_key=True)
    house_num = models.CharField(max_length=50)
    city = models.CharField(max_length=32)
    county = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    comm_name = models.CharField(max_length=32)
    price = models.IntegerField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    area = models.IntegerField()
    orientation = models.CharField(max_length=10)
    priceunit = models.CharField(max_length=10, blank=True, null=True)
    check_in_time = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    lift = models.CharField(max_length=10)
    car_station = models.CharField(max_length=10)
    water = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    gas = models.CharField(max_length=4)
    lease_term = models.CharField(max_length=20)
    rent_share = models.CharField(max_length=20)
    house_style = models.CharField(max_length=20)
    furniture = models.CharField(max_length=128)
    metro = models.IntegerField()
    detail_link = models.CharField(max_length=32)
    userid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_house_info'


class TbHouseType(models.Model):
    typeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_house_type'


class TbLoginLog(models.Model):
    logid = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    ipaddr = models.CharField(max_length=255)
    logdate = models.DateTimeField(blank=True, null=True)
    devcode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_log'


class TbUser(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=32)
    tel = models.CharField(unique=True, max_length=20)
    regdate = models.DateTimeField(blank=True, null=True)
    lastvisit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'
