# _*_coding:utf-8_*_
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from djcelery.views import JsonResponse

from scripts.models import Scripts, Country, Province, City, CountryChoice, ProvinceChoice, CityChoice
from apks.models import Apps, AppChoice
from devices.models import Devices, DeviceChoice
from sdks.models import Sdks, SdkChoice
from django.utils import timezone

work_dir = os.path.expanduser('~')
upload_path = os.path.join(work_dir, 'uploads')


@login_required()
def index(request):
    return render(request, 'scripts/index.html')


@login_required()
def create(request):
    user = User.objects.get(username=request.user.username)
    data = {
        'apks': [i.app_id for i in Apps.objects.filter(create_user=user)],
        'devices': ['%s_%s' % (i.id, i.device_model) for i in
                    Devices.objects.filter(create_user=user)],
        'sdks': [i.version for i in Sdks.objects.filter(create_user=user)],
        'country': Country.objects.all(),
        'province': Province.objects.all()}
    city = []
    for item in City.objects.all():
        city.append({'id': item.id, 'province': item.province.id, 'name': item.name})
    return render(request, 'scripts/create.html', {'data': data, 'city': city})


def save_file(p, files):
    if files:
        f = open(os.path.join(p, str(files.name)), 'wb+')
        for chunk in files.chunks():
            f.write(chunk)
        f.close()


def app_choice_create(script, apps, flag):
    for a in apps:
        try:
            AppChoice.objects.update_or_create(script=script,
                                               defaults={'app': Apps.objects.get(app_id=a), 'is_issued': flag})
        except Exception as e:
            print e
        else:
            continue


def device_choice_create(script, devices, flag):
    for d in devices:
        try:
            DeviceChoice.objects.update_or_create(script=script,
                                                  defaults={'device': Devices.objects.get(id=d.split('_')[0]),
                                                            'is_issued': flag})
        except Exception as e:
            print e
        else:
            continue


def sdk_choice_create(script, sdks, flag):
    for s in sdks:
        try:
            SdkChoice.objects.update_or_create(script=script,
                                               defaults={'sdk': Sdks.objects.get(version=s), 'is_issued': flag})
        except Exception as e:
            print e
        else:
            continue


def province_choice_create(script, provinces, flag):
    for p in provinces:
        try:
            ProvinceChoice.objects.update_or_create(script=script, defaults={'province': Province.objects.get(id=p),
                                                                             'is_issued': flag})
        except Exception as e:
            print e
        else:
            continue


def city_choice_create(script, citys, flag):
    for c in citys:
        try:
            CityChoice.objects.update_or_create(script=script,
                                                defaults={'city': City.objects.get(id=c), 'is_issued': flag})
        except Exception as e:
            print e
        else:
            continue


@login_required()
def save(request):
    request_data = request.POST
    data_type = request_data.get('dataType')
    time_slot_limit = request_data.get('inputTimeLimit')
    state = request_data.get('scriptState')
    effective_time = request_data.get('effectiveTime')
    invalid_time = request_data.get('invalidTime')
    task_type = request_data.get('taskType')
    os_type = request_data.get('osType')
    name = request_data.get('inputScriptName')
    hot = request_data.get('inputScriptHot')
    number = request_data.get('inputScriptNumber', 1)
    url = request_data.get('inputUrl')
    class_name = request_data.get('inputClassName')
    method_name = request_data.get('inputMethodName')
    throttle = request_data.get('inputThrottle')
    issued_time = request_data.get('inputIssuedTime')
    exec_time = request_data.get('inputExecuteTime')
    issued_limit_type = request_data.get('issuedLimitType')
    issued_count = request_data.get('inputIssuedCount')
    single_issued_count = request_data.get('inputSingleIssuedCount')
    upload_success_count = request_data.get('uploadSuccessCount')
    upload_fail_count = request_data.get('uploadFailCount')
    issued_os_version = request_data.get('issuedOsVersion')
    shield_os_version = request_data.get('shieldOsVersion')
    issued_app = request_data.getlist('issuedApp')
    shield_app = request_data.getlist('shieldApp')
    issued_device = request_data.getlist('issuedDevice')
    shield_device = request_data.getlist('shieldDevice')
    issued_sdk = request_data.getlist('issuedSdk')
    shield_sdk = request_data.getlist('shieldSdk')
    # issued_country = request_data.get('issuedCountry') //默认中国
    issued_province = request_data.get('issuedProvince')
    shield_province = request_data.get('shieldProvince')
    issued_city = request_data.get('issuedCity')
    shield_city = request_data.get('shieldCity')
    script_file = request.FILES.get('inputScriptFile')
    key_file = request.FILES.get('inputKeyFile')
    direct_uuid_file = request.FILES.get('inputUUIDFile')
    script_id = request.POST.get('id')
    if script_id:
        try:
            script = Scripts.objects.get(id=script_id)
        except Exception as e:
            print e
        else:
            script.time_slot_limit = time_slot_limit
            script.name = name
            script.number = number
            script.state = state
            script.task_type = task_type
            script.os_type = os_type
            script.hot = hot
            script.url = url
            script.effective_time = effective_time
            script.invalid_time = invalid_time
            script.update_time = timezone.now()
            script.class_name = class_name
            script.method_name = method_name
            script.throttle = throttle
            script.issued_delay = issued_time
            script.exec_delay = exec_time if exec_time else 0
            script.issued_limit_type = issued_limit_type
            script.issued_count = issued_count if issued_limit_type else -1
            script.single_issued_count = single_issued_count if issued_limit_type else -1
            script.upload_success = upload_success_count if upload_fail_count else -1
            script.upload_fail = upload_fail_count if upload_fail_count else -1
            script.issued_os_version = str(issued_os_version)
            script.shield_os_version = str(shield_os_version)
            script.script_file_path = script_file.name if script_file else ''
            script.key_file_path = key_file.name if key_file else ''
            script.direct_uuid_file = direct_uuid_file.name if direct_uuid_file else ''
            script.save()
            script_path = os.path.join(upload_path, request.user.username, data_type,
                                       script.update_time.strftime('%Y-%m-%d %H-%M-%S'),
                                       str(number), str(script.id))
            if not os.path.exists(script_path):
                os.makedirs(script_path)
            save_file(script_path, script_file)
            save_file(script_path, key_file)
            save_file(script_path, direct_uuid_file)
            app_choice_create(script, issued_app, 1)
            app_choice_create(script, shield_app, 0)
            device_choice_create(script, issued_device, 1)
            device_choice_create(script, shield_device, 0)
            sdk_choice_create(script, issued_sdk, 1)
            sdk_choice_create(script, shield_sdk, 0)
            province_choice_create(script, issued_province, 1)
            province_choice_create(script, shield_province, 0)
            city_choice_create(script, issued_city, 1)
            city_choice_create(script, shield_city, 0)
    else:
        with transaction.atomic():
            try:
                script = Scripts.objects.create(create_user=request.user,
                                                data_type=data_type,
                                                time_slot_limit=time_slot_limit,
                                                name=name,
                                                number=number,
                                                state=state,
                                                task_type=task_type,
                                                os_type=os_type,
                                                hot=hot,
                                                url=url,
                                                effective_time=effective_time, invalid_time=invalid_time,
                                                update_time=timezone.now(),
                                                class_name=class_name, method_name=method_name,
                                                throttle=throttle, issued_delay=issued_time, exec_delay=exec_time,
                                                issued_limit_type=issued_limit_type,
                                                issued_count=issued_count if issued_count else -1,
                                                single_issued_count=single_issued_count if single_issued_count else -1,
                                                upload_success=upload_success_count if upload_fail_count else -1,
                                                upload_fail=upload_fail_count if upload_fail_count else -1,
                                                issued_os_version=str(issued_os_version),
                                                shield_os_version=str(shield_os_version),
                                                script_file_path=script_file.name,
                                                key_file_path=key_file.name,
                                                direct_uuid_file=direct_uuid_file.name if direct_uuid_file else '')
            except Exception as e:
                print e
            else:
                script_path = os.path.join(upload_path, request.user.username, data_type,
                                           script.update_time.strftime('%Y-%m-%d %H-%M-%S'),
                                           str(number), str(script.id))
                if not os.path.exists(script_path):
                    os.makedirs(script_path)
                save_file(script_path, script_file)
                save_file(script_path, key_file)
                save_file(script_path, direct_uuid_file)
                app_choice_create(script, issued_app, 1)
                app_choice_create(script, shield_app, 0)
                device_choice_create(script, issued_device, 1)
                device_choice_create(script, shield_device, 0)
                sdk_choice_create(script, issued_sdk, 1)
                sdk_choice_create(script, shield_sdk, 0)
                CountryChoice.objects.create(script=script, country=Country.objects.get(id=1),
                                             is_issued=1)
                province_choice_create(script, issued_province, 1)
                province_choice_create(script, shield_province, 0)
                city_choice_create(script, issued_city, 1)
                city_choice_create(script, shield_city, 0)
    return HttpResponseRedirect(reverse('scripts:index'))


@login_required()
def search(request):
    data = []
    app_id = ''
    for i in Scripts.objects.filter(create_user=User.objects.filter(username=request.user.username)):
        try:
            app_choice = AppChoice.objects.filter(script=i).filter(is_issued=1)
            apps = [Apps.objects.get(id=a.app_id) for a in app_choice]
            app_id = str([j.app_id for j in apps])
        except Exception as e:
            print e
        data.append(
            {'id': i.id, 'data_type': i.data_type, 'os': 'android' if i.os_type else 'ios', 'name': i.name,
             'url': i.url, 'single_issued_limit': i.single_issued_count, 'app': app_id,
             'issued_limit_type': '根据上报计数' if i.issued_limit_type else '根据下发计数',
             'issued_count': i.issued_count, 'number': i.number,
             'effective_time': i.effective_time, 'invalid_time': i.invalid_time,
             'state': i.state, 'update_time': i.update_time.strftime('%Y-%m-%d %H:%M:%S'), 'hot': i.hot})
    return JsonResponse({'data': data})


@login_required()
def edit(request):
    try:
        script = Scripts.objects.get(id=request.GET.get('t', ''))
    except Exception as e:
        print e
        return render(request, 'scripts/create.html', {'data': {}})
    else:
        return render(request, 'scripts/create.html', {'data': script})


@login_required()
def delete(request):
    try:
        Scripts.objects.get(id=request.GET.get('t')).delete()
    except Exception as e:
        print e
    return render(request, 'scripts/index.html')


@login_required()
def online(request):
    try:
        script = Scripts.objects.get(id=request.GET.get('t'))
    except Exception as e:
        print e
    else:
        script.state = 0
        script.save()
    return render(request, 'scripts/index.html')


@login_required()
def offline(request):
    try:
        script = Scripts.objects.get(id=request.GET.get('t'))
    except Exception as e:
        print e
    else:
        script.state = 1
        script.save()
    return render(request, 'scripts/index.html')
