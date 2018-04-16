# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Scripts(models.Model):
    script_name = models.CharField(verbose_name=u'SCRIPT名称', max_length=50)
    url = models.TextField(verbose_name=u'SCRIPTURL地址', null=True)
    singleissued_count = models.IntegerField(verbose_name=u'SCRIPT单用户下发量', default=-1)
    app_id = models.IntegerField(verbose_name=u'SCRIPTAPPID')
    script_number = models.TextField(verbose_name=u'SCRIPT编号', null=True)
    dissued_count = models.IntegerField(verbose_name=u'SCRIPT日下发量', default=-1)
    effective_time = models.TextField(verbose_name=u'SCRIPT生效时间', null=True)
    dead_time = models.TextField(verbose_name=u'SCRIPT失效时间', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now_add=True)
    script_hot = models.IntegerField(verbose_name=u'SCRIPTR热度', null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = u'SCRIPT'
        db_table = 'scripts_manager'
