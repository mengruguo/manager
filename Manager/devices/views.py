# _*_coding:utf-8_*_
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from devices.models import Devices


@login_required()
def index(request):
    return render(request, 'devices/index.html')


@login_required()
def create(request):
    return render(request, 'devices/create.html')


@login_required()
def save(request):
    devices_id = request.POST.get('id')
    device_firm = request.POST.get('inputDeviceFirm')
    device_model = request.POST.get('inputDeviceModel')
    device_version = request.POST.get('inputDeviceVersion')
    if devices_id:
        devices = Devices.objects.get(id=devices_id)
        devices.device_firm = device_firm
        devices.device_model = device_model
        devices.version = device_version
        devices.save()
    else:
        with transaction.atomic():
            Devices.objects.create(device_firm=device_firm, create_user=request.user, device_model=device_model,
                                   version=device_version,
                                   update_time=timezone.now())
    return HttpResponseRedirect(reverse('devices:index'))


def search(request):
    data = []
    for i in Devices.objects.filter(create_user=User.objects.get(username=request.user.username)):
        data.append(
            {'id': i.id, 'manufacturer': i.device_firm, 'model': i.device_model, 'version': i.version,
             'update_time': i.update_time})
    return JsonResponse({'data': data})


@login_required()
def edit(request):
    try:
        device = Devices.objects.get(id=request.GET.get('t', ''))
    except Exception as e:
        print e
    else:
        data = {'id': device.id, 'device_firm': device.device_firm, 'device_model': device.device_model,
                'version': device.version}
    return render(request, 'devices/create.html', {'data': data})


@login_required()
def delete(request):
    try:
        Devices.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'devices/index.html')
