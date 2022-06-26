#! /usr/bin/python3
# Binh Nguyen, Feb26, 2020
# run multiple SDS011

import subprocess
import os
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
    usbs = get_usb()
    processs = list()
    for port in usbs:
        p = SDS011(port=port, push_mqtt=True, interval=int(os.environ['SDS_INTERVAL']))
        processs.append(p)
    while True:
        for p in processs:
            try:
                p.run_passive()
            except Exception as e:
                print(f'Error: {p.name} with {e}')
                continue
