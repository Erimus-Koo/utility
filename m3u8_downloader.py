#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
下载m3u8地址的视频文件
'''

import os
from erimus.toolbox import readClip, request, UA_PC, download, use_proxy
import fire

# ═══════════════════════════════════════════════
OUTPUT_PATH = 'G:\\Downloads\\'
TEMP_PATH = os.path.join(OUTPUT_PATH, 'm3u8_download_temp')
NAME = 'm3u8_download_temp'
# ═══════════════════════════════════════════════


def time2sec(time_str):
    ts = ('000000' + str(time_str))[-6:]
    return int(ts[:2]) * 3600 + int(ts[2:4]) * 60 + int(ts[4:6])


def m3u8_downloader(url=None, start=0, end=95959, OUTPUT_PATH=OUTPUT_PATH, NAME=NAME):
    url = url or readClip()  # 输入url 没有输入的话直接读取剪贴板
    print(f'{url = }')
    if not url.startswith('http') or 'm3u8' not in url:
        print('Please copy url of m3u8 first, then run this function.')
        return

    start = time2sec(start)
    end = time2sec(end)

    url_without_param = url.split('?')[0] if '?' in url else url
    domain_here = '/'.join(url_without_param.split('/')[:-1]) + '/'  # 当前路劲
    domain_root = '/'.join(domain_here.split('/')[:3])  # 根域名
    print(f'{domain_here=}')
    print(f'{domain_root=}')

    body = request(url)
    print(body)

    # 如果获得的是一个清晰度跳转列表 跳转并获取媒体文件列表 但保持domain不变
    if '#EXTINF' not in body and '#EXT-X-STREAM-INF' in body:
        last = ''
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                last = lines[i + 1]
        body = request(domain_here + last)
        print(body)

    slice_list = []
    now = 0
    for line in body.split('\n'):
        line = line.strip()
        if not line.startswith('#') and start < now < end:
            if not line.startswith('http'):  # 补全根目录
                if line.startswith('/'):
                    line = domain_root + line
                else:
                    line = domain_here + line
            slice_list.append(line)
        if line.startswith('#EXTINF:'):
            now += float(line.strip('#EXTINF:,'))

    for index, url in enumerate(slice_list):
        print(f'=== {index+1} / {len(slice_list)} ===')
        download(url, TEMP_PATH, f'{NAME}_{index:04d}.ts')

    temp_files = ''
    for path, dirs, files in os.walk(TEMP_PATH):  # read all files
        for fn in files:
            if fn.startswith(NAME) and fn.split('.')[-1] in ['ts']:
                file = os.path.join(path, fn)  # full path
                temp_files += f"file '{file}'\n"

    temp_videos = os.path.join(TEMP_PATH, f'{NAME}_videos.txt')
    with open(temp_videos, 'w', encoding='utf-8') as f:
        f.write(temp_files)

    out = os.path.join(OUTPUT_PATH, f'{NAME}.mp4')
    cmd = f'ffmpeg -f concat -safe 0 -i "{temp_videos}" -c copy "{out}"'
    print(f'>>> {cmd}')
    os.system(cmd)

    if os.path.exists(out):
        print(f'Downlaod finished: {out}')
        os.system(f'del {TEMP_PATH}\\{NAME}*.*')
        os.system(f'rmdir {TEMP_PATH}')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    # fire.Fire(m3u8_downloader)

    use_proxy()

    m3u8_downloader()
