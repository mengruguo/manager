# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from scripts.models import Scripts


# Create your models here.
class Sdks(models.Model):
    create_user = models.ForeignKey(User, verbose_name=u'sdk创建者')
    version = models.CharField(verbose_name=u'SDK版本', max_length=50)
    remark = models.TextField(verbose_name=u'SDK备注', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
    sdk = models.ManyToManyField(Scripts, verbose_name=u'sdk', through='SdkChoice')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'SDK'
        db_table = 'sdks_manager'


class SdkChoice(models.Model):
    script = models.ForeignKey(Scripts, related_name='sdk_choice_set')
    sdk = models.ForeignKey(Sdks, related_name='sdk_set')
    is_issued = models.BooleanField(verbose_name=u'是否支持下发', default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'sdks_choice'
        verbose_name = verbose_name_plural = u'SDK选择'
