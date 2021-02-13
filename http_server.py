#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 以本机 ip 启动 http server

import socket
from art import *
import os

# ═══════════════════════════════════════════════


def main():
    # get host ip
    hostname = socket.gethostname()
    print(f'{hostname = }')
    ip = socket.gethostbyname(hostname)
    print(f'{ip = }')

    valid = True
    for seg in ip.split('.'):
        if not seg.isdigit():
            valid = False
    if not valid:
        raise ValueError(f'Error: {ip}')

    tprint(ip, 'wizard')

    cmd = f"sudo python3 -m http.server 80 --directory /Users/erimus/OneDrive/site --bind {ip}"
    print(f'{cmd = }')
    os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    main()
