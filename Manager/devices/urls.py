#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time    : 2018/3/26 19:24
# @Author  : 6005001639
# @FileName: urls.py.py
# @Software: PyCharm Community Edition

from django.conf.urls import url

from views import *

app_name = 'devices'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create', create, name='create')
]
