# _*_coding:utf-8_*_
from django.shortcuts import render


def index(request):
    return render(request, 'devices/index.html')


def create(request):
    # app_id=
    return render(request, 'devices/index.html')
