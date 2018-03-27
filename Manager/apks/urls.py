# -*- coding: utf-8 -*-
from django.conf.urls import url

from views import *

app_name = 'apks'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create', create, name='create')
]
