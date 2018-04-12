# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from models import Apps


def index(request):
    return render(request, 'apks/index.html')


def create(request):
    return render(request, 'apks/create.html')


def save(request):
    apks_id = request.POST.get('id')
    app_name = request.POST.get('inputAppName')
    app_version = request.POST.get('inputAppVersion')
    if apks_id:
        apk = Apps.objects.get(id=apks_id)
        apk.name = app_name
        apk.version = app_version
        apk.save()
    else:
        if Apps.objects.count():
            app_id = Apps.objects.last().app_id + 1
        else:
            app_id = 10000
        with transaction.atomic():
            Apps.objects.create(app_id=app_id, name=app_name, version=app_version, update_time=timezone.now())
    return HttpResponseRedirect(reverse('apks:index'))


def search(request):
    data = []
    for i in Apps.objects.all():
        data.append(
            {'id': i.id, 'app_id': i.app_id, 'name': i.name, 'version': i.version, 'update_time': i.update_time})
    return JsonResponse({'data': data})


def edit(request):
    try:
        app = Apps.objects.get(id=request.GET.get('t', ''))
    except Exception as e:
        print e
    else:
        data = {'id': app.id, 'name': app.name, 'version': app.version}
    return render(request, 'apks/create.html', {'data': data})


def delete(request):
    try:
        Apps.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'apks/index.html')
