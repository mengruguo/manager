# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ScriptState(object):
    ONLINE = 0
    OFFLINE = 1
    DIRECT = 2


class Scripts(models.Model):
    create_user = models.ForeignKey(User, verbose_name=u'脚本创建者')
    data_type = models.CharField(verbose_name=u'数据类型', max_length=20)
    time_slot_limit = models.TextField(verbose_name=u'时段限制', null=True)
    name = models.CharField(verbose_name=u'脚本名称', max_length=50)
    number = models.IntegerField(verbose_name=u'脚本编号', default=1)
    state = models.IntegerField(verbose_name=u'状态', default=0, choices=(
        (ScriptState.ONLINE, u'上线'),
        (ScriptState.OFFLINE, u'下线'),
        (ScriptState.DIRECT, u'定向测试')
    ))
    task_type = models.IntegerField(verbose_name=u'任务类型', default=0, choices=((0, u'持续性'), (1, u'一次性')))
    os_type = models.IntegerField(verbose_name=u'系统类型', default=0, choices=((0, 'android'), (1, 'ios')))
    hot = models.IntegerField(verbose_name=u'热度', null=True)
    effective_time = models.CharField(verbose_name=u'生效时间', max_length=50, null=True)
    invalid_time = models.CharField(verbose_name=u'失效时间', max_length=50, null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True, null=True)
    url = models.TextField(verbose_name=u'URL地址', null=True)
    class_name = models.CharField(verbose_name=u'类名', max_length=50, default='')
    method_name = models.CharField(verbose_name=u'方法名', max_length=50, default='')
    throttle = models.IntegerField(verbose_name=u'间隔时间.时间单位分钟', default=0)
    issued_delay = models.IntegerField(verbose_name=u'下发延时.时间单位小时', default=0)
    exec_delay = models.IntegerField(verbose_name=u'执行延时.时间单位秒', default=0)
    issued_limit_type = models.IntegerField(verbose_name=u'下发限制计数类型', default=0, choices=(
        (0, u'根据下发计数'),
        (1, u'根据上报计数')))
    issued_count = models.IntegerField(verbose_name=u'下发限量', default=-1)
    single_issued_count = models.IntegerField(verbose_name=u'单用户下发限量', default=-1)
    upload_success = models.IntegerField(verbose_name=u'上报成功计数', default=-1)
    upload_fail = models.IntegerField(verbose_name=u'上报失败计数', default=-1)
    issued_os_version = models.CharField(verbose_name=u'下发系统版本', max_length=30, null=True)
    shield_os_version = models.CharField(verbose_name=u'屏蔽系统版本', max_length=30, null=True)
    script_file_path = models.CharField(verbose_name=u'脚本文件名', max_length=100, default=1)
    key_file_path = models.CharField(verbose_name=u'密钥文件名', max_length=100, null=True)
    direct_uuid_file = models.CharField(verbose_name=u'定向UUID文件名', max_length=100, null=True)

    @property
    def time_slot_limit(self):
        try:
            return eval(self._time_slot_limit)
        except SyntaxError:
            return []

    @time_slot_limit.setter
    def time_slot_limit(self, value):
        self._time_slot_limit = str(value)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'脚本'
        db_table = 'scripts_manager'


class Country(models.Model):
    name = models.CharField(u'国家名', max_length=50)
    country = models.ManyToManyField(Scripts, verbose_name=u'country', through='CountryChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'国家'
        db_table = 'scripts_country'


class Province(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'国家')
    name = models.CharField(u'省份名', max_length=100)
    province = models.ManyToManyField(Scripts, verbose_name=u'province', through='ProvinceChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'省份'
        db_table = 'scripts_province'


class City(models.Model):
    province = models.ForeignKey(Province, verbose_name=u'省份')
    name = models.CharField(u'城市名', max_length=100)
    city = models.ManyToManyField(Scripts, verbose_name=u'city', through='CityChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'城市'
        db_table = 'scripts_city'


class CountryChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='country_choice_set')
    country = models.ForeignKey(Country, related_name='country_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'country_choice'
        verbose_name = verbose_name_plural = u'国家选择'


class ProvinceChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='province_choice_set')
    province = models.ForeignKey(Province, related_name='province_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'province_choice'
        verbose_name = verbose_name_plural = u'省份选择'


class CityChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='city_choice_set')
    city = models.ForeignKey(City, related_name='city_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'city_choice'
        verbose_name = verbose_name_plural = u'城市选择'
