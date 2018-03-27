# -*- coding: utf-8 -*-
from django.conf.urls import url

from views import *

app_name = 'scripts'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create', create, name='create')
]