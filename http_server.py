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
        root = ('D:/OneDrive/site' if os.name == 'nt'
                else '/Users/erimus/OneDrive/site')
    else:
        root = root.replace('\\', '/')

    # get host ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f'{ip = }')

    valid = True
    for seg in ip.split('.'):
        if not seg.isdigit():
            valid = False
    if not valid:
        raise ValueError(f'Error: {ip}')

    tprint(ip, 'wizard')

    python = 'python' if os.name == 'nt' else 'sudo python3'  # mac need sudo sometime
    cmd = f'{python} -m http.server {port} --directory "{root}" --bind {ip}'
    print(f'{cmd = }')
    os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(http_server)
