# -*- coding: utf-8 -*-
from django.conf.urls import url

from views import *

app_name = 'scripts'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create', create, name='create'),
    url(r'^save', save, name='save'),
    url(r'^search', search, name='search'),
    url(r'^edit', edit, name='edit'),
    url(r'^delete', delete, name='delete'),
    url(r'^online', online, name='online'),
    url(r'^offline', offline, name='offline'),
    url(r'^all', alloffline, name='all')
]