# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Apps(models.Model):
    app_id = models.IntegerField(verbose_name=u'APPID', default=10000)
    name = models.CharField(verbose_name=u'APP名称', max_length=50)
    version = models.TextField(verbose_name=u'APP版本', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'APP'
        db_table = 'apps_manager'
