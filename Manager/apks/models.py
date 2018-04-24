# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from scripts.models import Scripts


class Apps(models.Model):
    app_id = models.IntegerField(verbose_name=u'APPID', default=10000)
    name = models.CharField(verbose_name=u'APP名称', max_length=50)
    version = models.TextField(verbose_name=u'APP版本', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
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
