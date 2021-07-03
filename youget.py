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
DEFAULT_PROXY = '127.0.0.1:7890'


def you_get(url, size='min', output_dir=None):
    # if proxy
    proxy = f'-x {DEFAULT_PROXY}' if 'youtube' in url else ''

    # find min/max size
    cmd = f'you-get {proxy} {url} -i'
    print(f'RUN COMMAND: {cmd}')
    p = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    out = p.decode('utf-8').replace('\n', '').replace('\r', '')
    itag_dict = {}
    for i in re.findall(r'\d+ bytes\)\s.*?=\d+', out):
        i = i.split(' ')
        itag_dict[i[-1]] = int(i[0])  # dict[itag] = size

    if not itag_dict:
        print(f'Request page has some error. ({__name__})')
        return 'error'

    itag = sorted(itag_dict.items(), key=lambda x: x[1],
                  reverse=(size == 'max'))[0][0]

    # download path = command running path
    path = f'-o {output_dir or os.getcwd()}'

    # download
    cmd = f'you-get {proxy} {url} {itag} {path}'
    print(f'RUN COMMAND: {cmd}')
    p = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    out = p.decode('utf-8')  # .replace('\n', '').replace('\r', '')
    # print(f'{out = }')
    if 'file already exists' in out:
        print(f' file already exists '.center(30, '-'))
        return 'exists'

    return 'success'


def main(*urls, size=None):  # download_size: min, max
    if not urls:
        print('Please input urls as args.\n>>> youget [url1] [url2] ...')
        return
    urls = [i for i in urls if i.startswith('http')][::-1]
    [print(url) for url in urls]
    for url in urls:
        you_get(url, size=size)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    main('https://www.youtube.com/watch?v=5KaDzxJP6vs')
    fire.Fire(main)
