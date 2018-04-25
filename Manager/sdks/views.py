# _*_coding:utf-8_*_
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from sdks.models import Sdks


@login_required()
def index(request):
    return render(request, 'sdks/index.html')


@login_required()
def create(request):
    return render(request, 'sdks/create.html')


@login_required()
def save(request):
    sdks_id = request.POST.get('id')
    sdk_version = request.POST.get('inputSdkName')
    sdk_remark = request.POST.get('inputSdkRemark')
    if sdks_id:
        sdks = Sdks.objects.get(id=sdks_id)
        sdks.version = sdk_version
        sdks.remark = sdk_remark
        sdks.save()
    else:
        with transaction.atomic():
            Sdks.objects.create(version=sdk_version, create_user=request.user, remark=sdk_remark,
                                update_time=timezone.now())
    return HttpResponseRedirect(reverse('sdks:index'))


def search(request):
    data = []
    for i in Sdks.objects.filter(create_user=User.objects.get(username=request.user.username)):
        data.append(
            {'id': i.id, 'version': i.version, 'remark': i.remark, 'update_time': i.update_time})
    print data
    return JsonResponse({'data': data})


@login_required()
def edit(request):
    data = {}
    try:
        sdk = Sdks.objects.get(id=request.GET.get('t', ''))
    except Exception as e:
        print e
    else:
        data = {'id': sdk.id, 'version': sdk.version, 'remark': sdk.remark}
    return render(request, 'sdks/create.html', {'data': data})


@login_required()
def delete(request):
    try:
        Sdks.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'sdks/index.html')
