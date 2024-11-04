#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
import time
from util.kill_process import kill_process

# ═══════════════════════════════════════════════


def find_icloud():
    for path, dirs, files in os.walk(
            'C:/Program Files/WindowsApps'):  # read all files
        # print(f'{dirs = }')
        for fn in files:
            if fn.lower() == 'iCloudDrive.exe'.lower():
                app = os.path.join(path, fn)  # full path
                print(f'{app = }')
                return app


def main(app=None):
    for p in ['iCloudDrive', 'iCloudPrefs', 'iCloudServices']:
        kill_process(p)
    time.sleep(3)

    app = app or find_icloud()
    os.system(f'"{app}"')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # app = 'C:/Program Files/WindowsApps/AppleInc.iCloud_13.4.101.0_x86__nzyj5cx40ttqa/iCloud/iCloudDrive.exe'
    main()

    # find_icloud()
