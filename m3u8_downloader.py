#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
下载m3u8地址的视频文件
'''

import os
import re
from erimus.toolbox import readClip, request, UA_PC, download, use_proxy
import fire

# ═══════════════════════════════════════════════
OUTPUT_PATH = 'G:\\Downloads\\'
TEMP_PATH = os.path.join(OUTPUT_PATH, 'm3u8_download_temp')
NAME = 'm3u8_download_temp'
CMD_BASE = 'ffmpeg -f concat -safe 0 -protocol_whitelist "file,http,https,tcp,tls"'
# ═══════════════════════════════════════════════


def time2sec(time_str):
    ts = ('000000' + str(time_str))[-6:]
    return int(ts[:2]) * 3600 + int(ts[2:4]) * 60 + int(ts[4:6])


def m3u8_downloader(url=None, start=0, end=95959,
                    OUTPUT_PATH=OUTPUT_PATH, NAME=NAME, method='split'):
    url = url or readClip()  # 输入url 没有输入的话直接读取剪贴板
    print(f'{url = }')
    if not url.startswith('http') or 'm3u8' not in url:
        print('Please copy url of m3u8 first, then run this function.')
        return

    # 格式化时间
    start = time2sec(start)
    end = time2sec(end)
    # 输出文件目录
    out = os.path.join(OUTPUT_PATH, f'{NAME}.mp4')

    url_without_param = url.split('?')[0] if '?' in url else url
    domain_here = '/'.join(url_without_param.split('/')[:-1]) + '/'  # 当前路劲
    domain_root = '/'.join(domain_here.split('/')[:3])  # 根域名
    print(f'{domain_here=}')
    print(f'{domain_root=}')

    body = request(url, retry_limit=99)
    print(f'body\n{body[:1000]}\n')

    # 如果获得的是一个清晰度跳转列表 跳转并获取媒体文件列表 但保持domain不变
    if '#EXTINF' not in body and '#EXT-X-STREAM-INF' in body:
        print('This is a m3u8 list!'.ljust(50, '='))
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                first = lines[i + 1]
                break
        print(f'Highest Resulution Address\n{domain_here + first}\n')
        body = request(domain_here + first)
        print(f'{"body".ljust(50,"=")}\n{body[:1000]}\n')

    # 补全视频片段地址
    slice_list = []
    now = 0  # 记录当前片段的起始秒数
    ext = None
    for line in re.findall(r'(?s)#EXTINF.*?(?=#)', body):
        time, address = line.split('\n')[:2]
        now += float(time.strip('#EXTINF:,'))

        if ext is None:
            ext = address.split('?')[0].split('.')[-1]

        if not address.startswith('http'):  # 补全根目录
            if address.startswith('/'):
                full_address = domain_root + address
            else:
                full_address = domain_here + address
        if start < now < end:
            slice_list.append(full_address)
            body = body.replace(address, full_address, 1)
    print(f'{"new body".ljust(50,"=")}\n{body[:1000]}')

    # 下载分片文件 并合并
    if method == 'split':
        # 下载分片
        temp_file_list = ''
        for index, url in enumerate(slice_list):
            print(f'=== {index+1} / {len(slice_list)} ===')
            temp_file = os.path.join(TEMP_PATH, f'{NAME}_{index:04d}.{ext}')
            while not os.path.exists(temp_file):  # try until downloaded
                download(url, TEMP_PATH, temp_file)
            temp_file_list += f"file '{temp_file}'\n"

        video_list_txt = os.path.join(TEMP_PATH, f'{NAME}.txt')
        with open(video_list_txt, 'w', encoding='utf-8') as f:
            f.write(temp_file_list)
        cmd = f'{CMD_BASE} -i {video_list_txt} -c copy "{out}"'

    # 直接用ffmpeg下载m3u8文件
    elif method == 'direct':
        m3u8_file = os.path.join(TEMP_PATH, f'{NAME}.m3u8')
        with open(m3u8_file, 'w', encoding='utf-8') as f:
            f.write(body)
        cmd = f'{CMD_BASE} -i "{m3u8_file}" -c copy "{out}"'

    print(f'{"+"*50}\n{cmd}\n{"+"*50}')
    os.system(cmd)

    if os.path.exists(out):
        print(f'Downlaod finished: {out}')
        # input('Press Enter to delete temp files?')
        if method == 'split':
            os.system(f'del {TEMP_PATH}\\{NAME}*.*')
        os.system(f'rmdir {TEMP_PATH}')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    # fire.Fire(m3u8_downloader)

    use_proxy()

    m3u8_downloader()
