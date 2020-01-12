#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 批量备份iPhone的照片及视频，先复制到指定路径，然后运行。
# 读取文件的各个时间，取其中最早的时间，以此改名。YYYYmmdd_HHMMSS.ext

import os
import logging as log
import exifread
from datetime import datetime
import time
import re

# ═══════════════════════════════════════════════


def format_time_str(t):
    return t.replace(':', '').replace('-', '').replace(' ', '_').replace('T', '_')


def ts2str(ts):
    return datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')


def rename_photo_by_time(root):
    renameList = []
    newNameDict = {}
    aaeList = []
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            fn = fn.lower()
            # 跳过已改名的文件
            year = root.split('/')[-1]
            if fn.startswith(year):
                continue

            file = os.path.join(path, fn)  # full path
            fn, ext = os.path.splitext(fn)

            # 删除aae文件
            if fn.endswith('aae'):
                aaeList.append(file)
                continue

            t = {}
            stat = os.stat(file)
            t['ctime'] = ts2str(int(stat.st_ctime))
            t['mtime'] = ts2str(int(stat.st_mtime))
            t['atime'] = ts2str(int(stat.st_atime))
            # [print(f'{k}: {ts2str(v)}') for k, v in t.items()]

            # read exif
            fd = open(file, 'rb')
            tags = exifread.process_file(fd)
            # [print(t, v) for t, v in tags.items()]
            fd.close()

            # [print(f'{k}: {v}') for k, v in tags.items()]
            if 'Image DateTime' in tags:
                t['stime'] = format_time_str(str(tags['Image DateTime']))
            if 'EXIF DateTimeOriginal' in tags:
                t['otime'] = format_time_str(tags['EXIF DateTimeOriginal'].values)
            t['dtime'] = ts2str(tags.get('DateTimeDigitized', time.time()))

            # read metadata
            with open(file, 'rb') as f:
                rr = re.findall(r'\d{4}[:\-]\d{2}[:\-]\d{2}[T ]\d{2}[:\-]\d{2}[:\-]\d{2}', str(f.read()))
                for i, iptct in enumerate(rr):
                    t[f'iptc{i}'] = format_time_str(iptct)

            print(f'{"="*30}\n{fn}{ext}')
            [print(f'  {k}: {v}') for k,v in t.items()]
            newName = min(t.values())  # most early

            # 同名文件自动加后缀
            newNameDict.setdefault(newName, 0)
            newNameDict[newName] += 1
            if newNameDict[newName] > 1:
                newName += f'({newNameDict[newName]})'

            if newName != fn:  # 跳过无须改名的文件
                renameList.append([fn + ext, newName + ext])
        break  # root only

    for file in aaeList:
        os.remove(file)

    print(f'\n{"="*30}\nRename List')
    for old, new in renameList:
        print(f'{old} --> {new}')
        old = os.path.join(root, old)
        new = os.path.join(root, new)
        os.rename(old, new)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    log.basicConfig(level=log.INFO, format=('pid:%(process)d | %(message)s'))

    root = 'D:/Downloads/photo backup'
    # root = 'D:/Downloads/temp'
    rename_photo_by_time(root)
