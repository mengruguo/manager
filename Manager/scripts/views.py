# _*_coding:utf-8_*_
from django.core.urlresolvers import reverse
from django.db import transaction

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from djcelery.views import JsonResponse

from scripts.models import Scripts


def index(request):
    return render(request, 'scripts/index.html')


def create(request):
    return render(request, 'scripts/create.html')


def save(request):
    scriptType = request.POST.get('inputDeviceFirm')
    osVer = request.POST.get('inputSysType')
    scriptName = request.POST.get('inputScriptName')
    url = request.POST.get('')
    oneIssuedCount = request.POST.get('inputOneIssuedLimit')
    issuedType = request.POST.get('inputIssuedCountType')
    scriptNumber = request.POST.get('inputScriptNumber')
    issuedCount = request.POST.get('inputIssuedLimit')
    effective_time = request.POST.get('inputShengxTime')
    dead_time = request.POST.get('inputShixTime')
    scriptSate = request.POST.get('inputDeviceState')
    scriptHot = request.POST.get('inputScriptHot')
    if Scripts.objects.count():
        appId = Scripts.objects.last().app_id + 1
    else:
        appId = 10000
    with transaction.atomic():
        Scripts.objects.create()
    return HttpResponseRedirect(reverse('apks:index'))


def search(request):
    data = []
    #
    return JsonResponse({'data': data})


def edit(request):
    data = []
    #
    return render(request, 'scripts/create.html', {'data': data})


def delete(request):
    try:
        Scripts.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'scripts/index.html')


def issued(request):
    # 下线
    return render(request, 'scripts/index.html')


def allissued(request):
    # 全部下线
    return render(request, 'scripts/index.html')
