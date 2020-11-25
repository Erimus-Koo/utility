#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
import time
from util.kill_process import kill_process

# ═══════════════════════════════════════════════


def main():
    for p in ['iCloudDrive', 'iCloudPrefs', 'iCloudServices']:
        kill_process(p)
    time.sleep(3)
    os.system('"C:/Program Files/WindowsApps/AppleInc.iCloud_11.4.12.0_x86__nzyj5cx40ttqa/iCloud/iCloudDrive.exe"')


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    main()
