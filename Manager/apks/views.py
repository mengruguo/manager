# -*- coding: utf-8 -*-
from django.shortcuts import render


def index(request):
    return render(request, 'apks/index.html')


def create(request):
    app_name = request.POST.get('inputAppName')
    app_version = request.POST.get('inputAppVersion')
    # app_id =
    return render(request, 'apks/create.html')
