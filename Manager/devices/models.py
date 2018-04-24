# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from scripts.models import Scripts


# Create your models here.
class Devices(models.Model):
    device_firm = models.CharField(verbose_name=u'DEVICE厂商', max_length=50)
    device_model = models.TextField(verbose_name=u'DEVICE设备型号', null=True)
    version = models.TextField(verbose_name=u'DEVICE操作系统版本', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
    scripts = models.ManyToManyField(Scripts, verbose_name=u'设备', through='DeviceChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'DEVICE'
        db_table = 'devices_manager'


class DeviceChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='device_choice_set')
    device = models.ForeignKey(Devices, related_name='device_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'devices_choice'
        verbose_name = verbose_name_plural = u'设备选择'
