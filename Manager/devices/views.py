# _*_coding:utf-8_*_
from django.shortcuts import render


def index(request):
    return render(request, 'devices/index.html')


def create(request):
    # app_id=
    device_firm = request.POST.get('inputDeviceFirm')
    device_model = request.POST.get('inputDeviceModel')
    device_version = request.POST.get('inputDeviceVersion')
    return render(request, 'devices/create.html')