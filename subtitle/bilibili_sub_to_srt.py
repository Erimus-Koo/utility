#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# B站下载的字幕文件 json -> srt

import json

# ═══════════════════════════════════════════════


def sec2hms(sec):
    return f'{int(sec//3600)}:{int(sec//60)}:{round(sec%60,2)}'


def bilibili_sub_to_srt(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    r = ''
    for i, sub in enumerate(data['body']):
        print(i, sub)
        r += (f"{i+1}\n{sec2hms(sub['from'])} --> {sec2hms(sub['to'])}\n"
              f"{sub['content']}\n\n")

    print(r)
    with open(file[:-4] + 'srt', 'w', encoding='utf-8') as f:
        f.write(r)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    file = 'D:/Downloads/av/Rams/《Rams》 -工业设计传奇设计师 迪特.拉姆斯2018纪录片（附中文字幕）.json'
    bilibili_sub_to_srt(file)
