# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Sdks(models.Model):
    version = models.CharField(verbose_name=u'SDK版本', max_length=50)
    remark = models.TextField(verbose_name=u'SDK备注', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'SDK'
        db_table = 'sdks_manager'
