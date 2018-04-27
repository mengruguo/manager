# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User

from models import Apps


@login_required()
def index(request):
    return render(request, 'apks/index.html')


@login_required()
def create(request):
    return render(request, 'apks/create.html')


@login_required()
def save(request):
    apks_id = request.POST.get('id')
    app_name = request.POST.get('inputAppName')
    app_version = request.POST.get('inputAppVersion')
    app_config = request.POST.get('inputAppConfig')
    if apks_id:
        apk = Apps.objects.get(id=apks_id)
        apk.name = app_name
        apk.version = app_version
        apk.config_time = app_config
        apk.save()
    else:
        if Apps.objects.count():
            app_id = Apps.objects.last().app_id + 1
        else:
            app_id = 10000
        with transaction.atomic():
            Apps.objects.create(app_id=app_id, name=app_name, create_user=request.user, version=app_version,
                                update_time=timezone.now(),
                                config_time=app_config if app_config else 5)
    return HttpResponseRedirect(reverse('apks:index'))


def search(request):
    data = []
    for i in Apps.objects.filter(create_user=User.objects.get(username=request.user.username)):
        data.append(
            {'id': i.id, 'app_id': i.app_id, 'name': i.name, 'version': i.version, 'update_time': i.update_time,
             'config_time': i.config_time})
    return JsonResponse({'data': data})


@login_required()
def edit(request):
    try:
        app = Apps.objects.get(id=request.GET.get('t', ''))
    except Exception as e:
        print e
    else:
        data = {'id': app.id, 'name': app.name, 'version': app.version, 'config_time': app.config_time}
    return render(request, 'apks/create.html', {'data': data})


@login_required()
def delete(request):
    try:
        Apps.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'apks/index.html')
