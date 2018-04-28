# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import os
from django.utils import timezone

from django.http import JsonResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from apks.models import Apps, Report
from scripts.models import Task, Scripts
from django.db.models import F

logger = logging.getLogger(__name__)
# WORK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK_DIR = os.path.expanduser('~')


def index(request):
    return render(request, 'index.html')


def manager(request):
    return render(request, 'index.html')


def config(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except ValueError:
            body = {}
        try:
            apps = Apps.objects.get(app_id=body.get('appId', 0) if type(body) == dict else 0)
        except Apps.DoesNotExist:
            return JsonResponse({'result': 5, 'msg': 'app is not exist'})
        else:
            return JsonResponse({'result': 0, 'msg': '', 'interval': apps.config_time})
    return HttpResponseForbidden()


def get(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except ValueError:
            body = {}
        try:
            apps = Apps.objects.get(app_id=body.get('appId', 0) if type(body) == dict else 0)
        except Apps.DoesNotExist:
            pass
        else:
            now = timezone.now()
            scripts = apps.app.order_by('-hot').filter(state=0).filter(effective_time__gt=now,
                                                                       invalid_time__lt=now).filter(
                issued_success__lt=F('issued_count'))

            if scripts.count():
                s = scripts.first()
                try:
                    new_s = Scripts.objects.get(id=s.id)
                except Exception as e:
                    print e
                else:
                    if not new_s.issued_limit_type:
                        new_s.issued_success += 1
                script_path = os.path.join(WORK_DIR, 'uploads', s.create_user, s.data_type,
                                           s.update_time.strftime('%Y-%m-%d %H:%M:%S'), s.id, s.script_file_path)
                if os.path.exists(script_path):
                    m = hashlib.md5()
                    with open(script_path, 'r') as f:
                        m.update(''.join(f.readlines()))
                    md5 = m.hexdigest()
                else:
                    md5 = ''
                t = Task.objects.create(script_type=int(s.data_type == 'js'), md5=md5, class_name=s.class_name,
                                        file_url='https://www.xxx.cn/%s' % s.script_file_path, exe_delay=s.exec_delay,
                                        function=s.method_name, task_type=s.task_type, script_number=s.number,
                                        count_limit_type=s.issued_limit_type, interval_time=s.throttle)
                return JsonResponse({'id': t.id, 'scriptType': t.script_type, 'fileUrl': t.file_url, 'md5': t.md5,
                                     'className': t.class_name, 'function': t.function, 'exeDelay': t.exe_delay,
                                     'countLimitType': t.count_limit_type, 'scriptNumber': t.script_number,
                                     'taskType': t.task_type, 'intervalTime': t.interval_time})
        return JsonResponse({'result': 5, 'msg': 'no task'})
    return HttpResponseForbidden()


def report(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except ValueError:
            body = {}
        try:
            apps = Apps.objects.get(app_id=body.get('appId', 0) if type(body) == dict else 0)
        except Apps.DoesNotExist:
            apps = None
        try:
            task = Task.objects.get(id=body.get('id', 0) if type(body) == dict else 0)
        except Task.DoesNotExist:
            task = None
        if apps and task:
            Report.objects.create(uuid=body.get('uuid'), apps=apps, phase=body.get('phase'), task=task,
                                  script_type=body.get('scriptType'), time=body.get('time'), imei=body.get('imei'),
                                  imsi=body.get('imsi'), mac=body.get('mac'), manufacturer=body.get('manufacturer'),
                                  model=body.get('model'), os_ver=body.get('osVer'), idfa=body.get('idfa'),
                                  err_msg=body.get('errmsg'), description=body.get('description'))
            return JsonResponse({'result': 0})
        else:
            return JsonResponse({'result': 5, 'msg': 'no apps or task'})
    return HttpResponseForbidden()
