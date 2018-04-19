# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from apks.models import Apps
from devices.models import Devices
from sdks.models import Sdks


class ScriptState(object):
    ONLINE = 0
    OFFLINE = 1
    DIRECT = 2


# Create your models here.
class Scripts(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=50)
    number = models.IntegerField(verbose_name=u'编号', default=1)
    state = models.IntegerField(verbose_name=u'状态', default=0, choices=(
        (ScriptState.ONLINE, u'上线'),
        (ScriptState.OFFLINE, u'下线'),
        (ScriptState.DIRECT, u'定向测试')
    ))
    task_type = models.IntegerField(verbose_name=u'任务类型', default=0, choices=((0, u'持续性'), (1, u'一次性')))
    os_type = models.IntegerField(verbose_name=u'系统类型', default=0, choices=((0, 'android'), (1, 'ios')))
    hot = models.IntegerField(verbose_name=u'热度', null=True)
    effective_time = models.TextField(verbose_name=u'生效时间', null=True)
    dead_time = models.TextField(verbose_name=u'失效时间', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
    url = models.TextField(verbose_name=u'URL地址', null=True)
    class_name = models.CharField(verbose_name=u'类名', max_length=50, default='')
    method_name = models.CharField(verbose_name=u'方法名', max_length=50, default='')
    throttle = models.IntegerField(verbose_name=u'间隔时间.时间单位分钟', default=0)
    issued_delay = models.IntegerField(verbose_name=u'下发延时.时间单位小时', default=0)
    exec_issued = models.IntegerField(verbose_name=u'执行延时.时间单位秒', default=0)
    issued_limit_type = models.IntegerField(verbose_name=u'下发限制计数类型', default=0, choices=(
        (0, u'根据下发计数'),
        (1, u'根据上报计数')))
    issued_count = models.IntegerField(verbose_name=u'下发限量', default=-1)
    single_issued_count = models.IntegerField(verbose_name=u'单用户下发限量', default=-1)
    upload_success = models.IntegerField(verbose_name=u'上报成功计数', default=-1)
    upload_fail = models.IntegerField(verbose_name=u'上报失败计数', default=-1)
    issued_os_version = models.CharField(verbose_name=u'下发系统版本', max_length=30, null=True)
    shield_os_version = models.CharField(verbose_name=u'屏蔽系统版本', max_length=30, null=True)
    app = models.ManyToManyField(Apps, verbose_name=u'app', through=AppChoice)
    device = models.ManyToManyField(Devices, verbose_name=u'设备', through=DeviceChoice)
    sdk = models.ManyToManyField(Sdks, verbose_name=u'sdk', through=SdkChoice)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'脚本'
        db_table = 'scripts_manager'


class AppChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='script_set')
    app = models.ForeignKey(Apps, related_name='app_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'app_choice'
        verbose_name = verbose_name_plural = u'app选择'

class DeviceChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='script_set')
    device = models.ForeignKey(Devices, related_name='device_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'device_choice'
        verbose_name = verbose_name_plural = u'设备选择'


class SdkChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='script_set')
    sdk = models.ForeignKey(Sdks, related_name='sdk_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'sdk_choice'
        verbose_name = verbose_name_plural = u'SDK选择'
