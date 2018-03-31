# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Devices(models.Model):
    device_firm = models.CharField(verbose_name=u'DEVICE厂商', max_length=50)
    device_model = models.TextField(verbose_name=u'DEVICE设备型号', null=True)
    version = models.TextField(verbose_name=u'DEVICE操作系统版本', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'DEVICE'
        db_table = 'devices_manager'
