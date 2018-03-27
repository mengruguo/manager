# -*- coding: utf-8 -*-

import logging
import os

from django.shortcuts import render

logger = logging.getLogger(__name__)
WORK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def index(request):
    return render(request, 'index.html')


def manager(request):
    return render(request, 'index.html')
