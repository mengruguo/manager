# -*- coding: utf-8 -*-
from django.conf.urls import url

from views import *

app_name = 'devices'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create', create, name='create')
]
