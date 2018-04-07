# _*_coding:utf-8_*_
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils import timezone

from sdks.models import Sdks


def index(request):
    return render(request, 'sdks/index.html')


def create(request):
    sdk_name = request.POST.get('inputSdkName')
    sdk_remark = request.POST.get('inputSdkRemark')
    return render(request, 'sdks/create.html')


def save(request):
    sdk_version = request.POST.get('inputSdkName')
    sdk_remark = request.POST.get('inputSdkRemark')
    with transaction.atomic():
        Sdks.objects.create(name=sdk_version, version=sdk_remark, update_time=timezone.now())
    return HttpResponseRedirect(reverse('sdks:index'))


def search(request):
    data = []
    for i in Sdks.objects.all():
        data.append(
            {'id': i.id, 'version': i.version, 'remark': i.remark, 'update_time': i.update_time})
    return JsonResponse({'data': data})
