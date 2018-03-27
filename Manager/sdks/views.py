# _*_coding:utf-8_*_
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'sdks/index.html')


def create(request):
    sdk_name = request.POST.get('inputSdkName')
    sdk_remark = request.POST.get('inputSdkRemark')
    return render(request, 'sdks/create.html')
