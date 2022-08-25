#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
下载m3u8地址的视频文件
'''

import os
import re
from erimus.toolbox import read_clip, request, UA_PC, download, use_proxy
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


def m3u8_downloader(
    url=None, start=0, end=95959, OUTPUT_PATH=OUTPUT_PATH, NAME=NAME,
    method='download_then_merge',  # 下载到本地并合并 或者直接ffmpeg下载
):
    url = url or read_clip()  # 输入url 没有输入的话直接读取剪贴板
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
    domain_here = '/'.join(url_without_param.split('/')[:-1]) + '/'  # 当前路径
    domain_root = '/'.join(domain_here.split('/')[:3])  # 根域名
    print(f'{domain_here=}')
    print(f'{domain_root=}')

    body = request(url, retry_limit=99)
    print(f'body\n{body[:1000]}\n')

    # 从清晰度列表 跳转并获取媒体文件列表 但保持domain不变
    if '#EXTINF' not in body and '#EXT-X-STREAM-INF' in body:
        print('This is a m3u8 list!'.ljust(50, '='))
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                first = lines[i + 1]
                break  # 取第一条
        if not first.startswith('http'):  # 补全根目录
            first = (domain_root if first[0] == '/' else domain_here) + first
        print(f'Highest Resulution Address\n{first}\n')
        body = request(first)
        print(f'{"body".ljust(50,"=")}\n{body[:1000]}\n')

    # 补全视频片段地址
    slice_list = []  # 视频片段列表
    online_m3u = []  # 补全域名的在线版的m3u文件
    local_m3u = []  # 补全域名的本地版的m3u文件
    now = v_index = 0  # 记录当前片段的起始秒数
    ext = None
    body = body.split('\n')
    while len(body):
        line = body.pop(0)
        print(f'{line = }')

        # 获取Key
        if line.startswith('#EXT-X-KEY:'):
            key_uri = re.search(r'(?<=URI=").*?(?=")', line)
            local_key = os.path.join(TEMP_PATH, f'{NAME}.key')
            if key_uri:
                key_uri = key_uri.group(0)
                download(key_uri, TEMP_PATH, f'{NAME}.key')
            print(f'{key_uri = }')
            online_m3u.append(line)
            local_m3u.append(line.replace(key_uri, local_key.replace('\\', '/')))

        # 获取视频链接
        elif line.startswith('#EXTINF:'):
            time, v_url = line, body.pop(0)
            now += float(time.strip('#EXTINF:,'))

            if not v_url.startswith('http'):  # 补全根目录
                fv_url = (domain_root if v_url[0] == '/' else domain_here) + v_url

            if ext is None:
                ext = v_url.split('?')[0].split('.')[-1]
            local_file = os.path.join(TEMP_PATH, f'{NAME}_{v_index:04d}.{ext}')

            if start < now < end:
                slice_list.append((fv_url, local_file))
                online_m3u += [time, fv_url]
                local_m3u += [time, local_file.replace('\\', '/')]
                v_index += 1

        else:
            online_m3u.append(line)
            local_m3u.append(line)
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)
    online_m3u8_file = os.path.join(TEMP_PATH, f'{NAME}_online.m3u8')
    local_m3u8_file = os.path.join(TEMP_PATH, f'{NAME}_local.m3u8')
    with open(online_m3u8_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(online_m3u))
    with open(local_m3u8_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(local_m3u))

    # 下载分片文件 并合并
    if method == 'download_then_merge':
        # 下载分片
        temp_file_list = ''
        for index, (v_url, local_file) in enumerate(slice_list):
            print(f'=== {index+1} / {len(slice_list)} ===')
            while not os.path.exists(local_file):  # try until downloaded
                download(v_url, TEMP_PATH, local_file)
            temp_file_list += f"file '{local_file}'\n"

        video_list_txt = os.path.join(TEMP_PATH, f'{NAME}.txt')
        with open(video_list_txt, 'w', encoding='utf-8') as f:
            f.write(temp_file_list)
        # cmd = f'{CMD_BASE} -i "{video_list_txt}" -c copy "{out}"'
        m3u8_file = local_m3u8_file
    else:
        m3u8_file = online_m3u8_file

    cmd = f'ffmpeg -allowed_extensions ALL -i "{m3u8_file}" -c copy "{out}"'
    print(f'{"+"*50}\n{cmd}\n{"+"*50}')
    os.system(cmd)

    if os.path.exists(out):
        print(f'Downlaod finished: {out}')
        # input('Press Enter to delete temp files?')
        if method == 'download_then_merge':
            os.system(f'del "{TEMP_PATH}\\{NAME}*.*"')
        os.system(f'rmdir "{TEMP_PATH}"')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    fire.Fire(m3u8_downloader)

    # use_proxy()

    # m3u8_downloader(start=100, end=200)
