# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from scripts.models import Scripts, Task


class Apps(models.Model):
    app_id = models.IntegerField(verbose_name=u'APPID', default=10000)
    name = models.CharField(verbose_name=u'APP名称', max_length=50)
    version = models.TextField(verbose_name=u'APP版本', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
    config_time = models.IntegerField(verbose_name=u'配置时间', default=5)
    app = models.ManyToManyField(Scripts, verbose_name=u'app', through='AppChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'APP'
        db_table = 'apps_manager'


class AppChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='app_choice_set')
    app = models.ForeignKey(Apps, related_name='app_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'apps_choice'
        verbose_name = verbose_name_plural = u'app选择'


class Report(models.Model):
    uuid = models.CharField(verbose_name=u'设备唯一ID', max_length=32)
    apps = models.ForeignKey(Apps, related_name='apps_set')
    phase = models.IntegerField(verbose_name=u'汇报状态', choices=((0, 'success'), (1, 'failure')))
    task = models.ForeignKey(Task, related_name='task_set')
    script_type = models.IntegerField(verbose_name=u'脚本类型', default=1, choices=((0, 'lua'), (1, 'js')))
    time = models.IntegerField(verbose_name=u'时间戳')
    imei = models.CharField(verbose_name=u'IMEI', max_length=15, null=True)
    imsi = models.CharField(verbose_name=u'IMSI', max_length=15, null=True)
    mac = models.CharField(verbose_name=u'MAC', max_length=17, null=True)
    idfa = models.CharField(verbose_name=u'IDFA', max_length=36, null=True)
    model = models.CharField(verbose_name=u'机型', max_length=15, null=True)
    os_ver = models.CharField(verbose_name=u'系统版本', max_length=15, null=True)
    manufacturer = models.CharField(verbose_name=u'厂商', max_length=15, null=True)
    err_msg = models.CharField(verbose_name=u'错误信息', max_length=100, null=True)
    description = models.CharField(verbose_name=u'补充描述', max_length=100, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'报告'
        db_table = 'apps_report'
