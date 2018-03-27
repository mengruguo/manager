# -*- coding: utf-8 -*-
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from models import Apps


def index(request):
    return render(request, 'apks/index.html')


def create(request):
    return render(request, 'apks/create.html')


def save(request):
    app_name = request.POST.get('inputAppName')
    app_version = request.POST.get('inputAppVersion')
    if Apps.objects.count():
        app_id = Apps.objects.last().app_id
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
    # data = Apps.objects.all()
    return JsonResponse({'data': data})
