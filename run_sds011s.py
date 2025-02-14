#! /usr/bin/python3
# Binh Nguyen, Feb26, 2020
# run multiple SDS011

import subprocess
import os
import traceback
from sds011 import SDS011


def get_usb():
    try:
        with subprocess.Popen(['ls /dev/ttyUSB*'], shell=True, stdout=subprocess.PIPE) as f:
            usbs = f.stdout.read().decode('utf-8')
        usbs = usbs.split('\n')
        usbs = [usb for usb in usbs if len(usb) > 3]
    except Exception as e:
        print('No USB available')
    return usbs


if __name__ ==  '__main__':
    print('Starting')
    usbs = get_usb()
    processs = list()
    for port in usbs:
        print(f'Using USB {port}')
        p = SDS011(port=port, push_mqtt=True, save_data=False, interval=int(os.environ['SDS_INTERVAL']))
        processs.append(p)
    while True:
        for p in processs:
            try:
                p.run_passive()
            except Exception as e:
                print(f'Error highest: {p.name} with {e}')
                print(traceback.format_exc())
                continue
