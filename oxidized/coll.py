import os
import time
import schedule
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakeTOoxidized.settings')
import django
django.setup()

from netmiko import ConnectHandler
from oxidized.models import Device, Oxidized
import difflib
from django.utils import timezone
from datetime import datetime


def backup_config(save=True):
    device_info = Device.objects.all()
    for info in device_info:
        name = info.name
        ip = info.ip
        username = info.username
        password = info.password
        port = info.port
        platform = info.platform
        group = info.group
    device = {
        'ip': ip,
        'username': username,
        'password': password,
        'device_type': platform,
        'port': port,
    }
    output = str()
    try:
        # update_time = time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime())
        update_time = timezone.now()
        with ConnectHandler(**device) as conn:
            if platform == 'huawei':
                output = conn.send_command('display cu')
            elif platform == 'hp-commware':
                output = conn.send_command('display cu')
            elif platform == 'cisco':
                output = conn.send_command('show running-config')
            # print(output)
        state = True
    except Exception as e:
        # print(e)
        state = False
    # 比对配置差异
    config = str()
    config_all = Oxidized.objects.all()
    for configs in config_all:
        config = configs.config
        # print('配置是%s' % config)
        last_change_time = configs.last_change
        shang_diff = configs.diff
    if config != '':
        output_lines = output.splitlines()
        config_lines = config.splitlines()
        # d = difflib.Differ()
        # diff = d.compare(output_lines, config_lines)
        diff = difflib.context_diff(output_lines, config_lines)
        differ = '\n'.join(list(diff))
        print(differ)
        # print(len(output_lines))
        # print(len(differ.splitlines()))
        if len(differ.splitlines()) == 0:
            change_time = last_change_time
            differ = shang_diff
            print('1')
        else:
            # change_time = time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime())
            change_time = timezone.now()
            # print('differ内容是%s' % differ)
            print('2')
    else:
        change_time = '1900-01-01 11:11:11'
        differ = 'null'
    if save:
            try:
                obj, created = Oxidized.objects.update_or_create(ip=ip,
                                                                 defaults=dict(name=name,
                                                                               ip=ip,
                                                                               group=group,
                                                                               platform=platform,
                                                                               last_update=update_time,
                                                                               state=state,
                                                                               last_change=change_time,
                                                                               config=output,
                                                                               diff=differ,
                                                                               ))

                print('设备%s保存成功' % ip)
            except Exception as e:
                print('设备%s保存失败，原因是%s' % (ip, str(e)))

def task_list():
    schedule.clear()
    schedule.every(60).seconds.do(backup_config)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    task_list()
