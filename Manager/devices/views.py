# _*_coding:utf-8_*_
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from devices.models import Devices


def index(request):
    return render(request, 'devices/index.html')


def create(request):
    return render(request, 'devices/create.html')


def save(request):
    device_firm = request.POST.get('inputDeviceFirm')
    device_model = request.POST.get('inputDeviceModel')
    device_version = request.POST.get('inputDeviceVersion')
    with transaction.atomic():
        Devices.objects.create(manufacturer=device_firm, devices_type=device_model, version=device_version,
                               update_time=timezone.now())
    return HttpResponseRedirect(reverse('devices:index'))


def search(request):
    data = []
    for i in Devices.objects.all():
        data.append(
            {'id': i.id, 'manufacturer': i.device_firm, 'devices_type': i.device_model, 'version': i.version,
             'update_time': i.update_time})
    return JsonResponse({'data': data})
