# _*_coding:utf-8_*_
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'scripts/index.html')


def create(request):
    # app_id=
    return render(request, 'scripts/index.html')
