# _*_coding:utf-8_*_
from django.core.urlresolvers import reverse
from django.db import transaction

from django.http import HttpResponseRedirect
from django.shortcuts import render
import os

# Create your views here.
from djcelery.views import JsonResponse

from scripts.models import Scripts, Country, Province, City, CountryChoice, ProvinceChoice, CityChoice
from apks.models import Apps, AppChoice
from devices.models import Devices, DeviceChoice
from sdks.models import Sdks, SdkChoice
from django.utils import timezone


def index(request):
    return render(request, 'scripts/index.html')


def create(request):
    data = {'apks': [i.app_id for i in Apps.objects.all()],
            'devices': ['%s_%s' % (i.id, i.device_model) for i in Devices.objects.all()],
            'sdks': [i.version for i in Sdks.objects.all()],
            'country': Country.objects.all(),
            'province': Province.objects.all()}
    city = []
    for item in City.objects.all():
        city.append({'id': item.id, 'province': item.province.id, 'name': item.name})
    return render(request, 'scripts/create.html', {'data': data, 'city': city})


def save_file(upload_path, files):
    f = open(os.path.join(upload_path, str(files.name)), 'wb+')
    for chunk in files.chunks():
        f.write(chunk)
    f.close()


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
    issued_country = request_data.get('issuedCountry')
    issued_province = request_data.get('issuedProvince')
    shield_province = request_data.get('shieldProvince')
    issued_city = request_data.get('issuedCity')
    shield_city = request_data.get('shieldCity')
    upload_path = os.path.join(os.path.expanduser('~'), name)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    script_file_path = ''
    key_file_path = ''
    direct_uuid_file = ''
    for files in request.FILES.getlist('inputScriptFile'):
        save_file(upload_path, files)
        script_file_path = '%s_%s' % (script_file_path, files.name)
    for files in request.FILES.getlist('inputKeyFile'):
        save_file(upload_path, files)
        key_file_path = '%s_%s' % (key_file_path, files.name)
    for files in request.FILES.getlist('inputUUIDFile'):
        save_file(upload_path, files)
        direct_uuid_file = '%s_%s' % (direct_uuid_file, files.name)
    script_id = request.POST.get('id')
    if script_id:
        script = Apps.objects.get(id=script_id)
        # TODO
        script.save()
    else:
        with transaction.atomic():
            try:
                script = Scripts.objects.create(data_type=data_type,
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
                                                script_file_path=script_file_path,
                                                key_file_path=key_file_path,
                                                direct_uuid_file=direct_uuid_file)
            except Exception as e:
                print e
            else:
                for app in issued_app:
                    AppChoice.objects.create(script=script, app=Apps.objects.get(app_id=app), is_issued=1)
                for app in shield_app:
                    AppChoice.objects.create(script=script, app=Apps.objects.get(app_id=app), is_issued=0)
                for d in issued_device:
                    DeviceChoice.objects.create(script=script, device=Devices.objects.get(id=d.split('_')[0]),
                                                is_issued=1)
                for d in shield_device:
                    DeviceChoice.objects.create(script=script, device=Devices.objects.get(id=d.split('_')[0]),
                                                is_issued=0)
                for s in issued_sdk:
                    SdkChoice.objects.create(script=script, sdk=Sdks.objects.get(version=s), is_issued=1)
                for s in shield_sdk:
                    SdkChoice.objects.create(script=script, sdk=Sdks.objects.get(version=s), is_issued=0)
                if issued_country:
                    CountryChoice.objects.create(script=script, country=Country.objects.get(id=issued_country),
                                                 is_issued=1)
                if issued_province:
                    ProvinceChoice.objects.create(script=script, province=Province.objects.get(id=issued_province),
                                                  is_issued=1)
                if int(shield_province):
                    ProvinceChoice.objects.create(script=script, province=Province.objects.get(id=shield_province),
                                                  is_issued=0)
                if issued_city:
                    CityChoice.objects.create(script=script, city=City.objects.get(id=issued_city), is_issued=1)
                if int(shield_city):
                    print shield_city
                    CityChoice.objects.create(script=script, city=City.objects.get(id=shield_city), is_issued=0)
    return HttpResponseRedirect(reverse('scripts:index'))


def search(request):
    data = []
    app_id = ''
    for i in Scripts.objects.all():
        try:
            app_choice = AppChoice.objects.filter(script=i).filter(is_issued=1)
            apps = [Apps.objects.get(id=a.app_id) for a in app_choice]
            app_id = str([j.app_id for j in apps])
        except Exception as e:
            print e
        data.append(
            {'id': i.id, 'data_type': i.data_type, 'os': 'android' if i.os_type else 'ios', 'name': i.name,
             'url': i.url, 'single_issued_limit': i.single_issued_count, 'app': app_id})
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
