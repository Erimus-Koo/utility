#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 简化you-get，自动判断是否使用代理，及获取最小格式。

import sys
import os
import subprocess
import re
import fire

# ═══════════════════════════════════════════════
DEFAULT_PROXY = '127.0.0.1:1080'


def you_get(url, download_size='min'):
    # if proxy
    proxy = f'-x {DEFAULT_PROXY}' if 'youtube' in url else ''

    # find min/max size
    cmd = f'you-get {proxy} {url} -i'
    print(f'RUN COMMAND: {cmd}')
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('utf-8').replace('\n', '').replace('\r', '')
    itag_dict = {}
    for i in re.findall(r'\d+ bytes\)\s.*?=\d+', out):
        i = i.split(' ')
        itag_dict[i[-1]] = int(i[0])  # dict[itag] = size
    itag = sorted(itag_dict.items(), key=lambda x: x[1],
                  reverse=(download_size == 'max'))[0][0]

    # download path = command running path
    path = f'-o {os.getcwd()}'

    # download
    cmd = f'you-get {proxy} {url} {itag} {path}'
    print(f'RUN COMMAND: {cmd}')
    os.system(cmd)


def main():  # download_size: min, max
    [print(arg) for arg in sys.argv]
    urls = [i for i in sys.argv[1:] if i.startswith('http')][::-1]
    [print(url) for url in urls]
    for url in urls:
        you_get(url)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(main)
