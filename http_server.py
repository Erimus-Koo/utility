#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 以本机 ip 启动 http server

import socket
from art import *
import os
import fire

# ═══════════════════════════════════════════════


def http_server(root=None, port=80):
    if root is None:
        root = 'D:/OneDrive/site' if os.name =='nt' else '/Users/erimus/OneDrive/site'
    else:
        root = root.replace('\\', '/')

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

    sudo = '' if os.name == 'nt' else 'sudo '  # mac need sudo sometime
    cmd = f'{sudo}python -m http.server {port} --directory "{root}" --bind {ip}'
    print(f'{cmd = }')
    os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(http_server)
