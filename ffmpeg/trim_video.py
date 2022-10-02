#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# use ffmpeg trim & merge video
# ffmpeg need to be added in PATH

import pyperclip
import os
import re
from datetime import datetime
import fire
import json

# ═══════════════════════════════════════════════
DL = '\n' + '-' * 50 + '\n'
# ═══════════════════════════════════════════════


def fmt_time(time_str):
    if time_str.count(':') == 1:
        return datetime.strptime(time_str, '%M:%S')
    else:
        return datetime.strptime(time_str, '%H:%M:%S')


def str_list(array):
    return [str(i) for i in array]


def int_list(array):
    return [int(i) for i in array]


class SaveInput():
    """保存输入的切割点"""

    def __init__(self, filename):
        self.filename = filename.upper()
        here = os.path.abspath(os.path.dirname(__file__))
        self.log_file = os.path.join(here, 'trim_video.log')
        with open(self.log_file, 'r', encoding='utf-8') as f:
            self._log_data = json.load(f)
        self._log_data.setdefault(self.filename, [])
        self.log = self._log_data[self.filename]

    def add(self, clip_points):
        # print(f'{clip_points = }')
        str_clip_points = " ".join([str(p) for p in clip_points])
        # print(f'{str_clip_points = }')
        self._log_data[self.filename] = str_clip_points
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._log_data, ensure_ascii=False, indent=2))


def trim_video(src_file=None, *clip_points, merge=True):
    print(f'{src_file = }\n{clip_points = }\n{merge = }\n---')
    src_file = src_file or pyperclip.paste()  # 没有输入的话直接读取剪贴板
    print(f'{src_file = }')
    assert os.path.isfile(src_file)
    path = os.path.abspath(os.path.dirname(src_file))
    full_file_name = os.path.basename(src_file)
    file_name, ext = os.path.splitext(full_file_name)
    print(f'{path=}\n{file_name=}\n{ext=}')

    out_file = os.path.join(path, f'{file_name}_trim{ext}')
    print(f'{out_file=}')

    # 读取存储的切割点
    saved = SaveInput(file_name)
    if saved.log:
        use_saved = input(f'Find saved clip points:\n{saved.log}\n(y/n):')
        if use_saved.lower() in ['y', '']:
            clip_points = saved.log.split(' ')
        elif use_saved.lower() == 'n':
            clip_points = []
        else:
            clip_points = [p for p in use_saved.split(' ') if p]
    print('Loaded:')
    [print(clip_points[i:i + 2]) for i in range(0, len(clip_points), 2)]

    # 输入切割点
    clip_points = clip_points or []
    while True:
        input_param = input('Input clip start & end: ')
        if input_param == 'end' or not input_param:
            break
        else:
            input_param = input_param.replace(':', '')
            clip_points += re.findall(r'\d+', input_param)
            int_clip_points = int_list(clip_points)
            if int_clip_points != sorted(int_clip_points):
                print(f'Time sorted error:\n'
                      f'{" ".join(str_list(clip_points))}')
                return
            clip_points = str_list(int_clip_points)
            saved.add(clip_points)
    print(f'{clip_points = }')

    clipset = []
    # fix clip points, for input 6 digit number without ':'.
    print(f'{clip_points=}')

    for i, c in enumerate(clip_points):
        if ':' not in c:
            c = ('000000' + c)[-6:]
            clip_points[i] = c[0:2] + ':' + c[2:4] + ':' + c[4:6]
    clip_points += ['23:59:59']
    # print(f'{clip_points=}')
    for i in range((len(clip_points)) // 2):
        clipset.append([clip_points[i * 2], clip_points[i * 2 + 1]])
    [print(i) for i in clipset]
    input('Press enter to continue...')

    videoList = []
    for i, [start, end] in enumerate(clipset):
        st = fmt_time(start)
        et = fmt_time(end)
        duration = str(et - st)
        print(f'{DL}{duration=}')
        trim_file = os.path.join(path, f'{file_name}_trim{i}{ext}')
        videoList.append(trim_file)
        trimCmd = (f'ffmpeg -ss {start} -t {duration} -i "{src_file}"'
                   f' -vcodec copy -acodec copy "{trim_file}"')
        print(f'{trimCmd = }{DL}')
        os.system(trimCmd)

    if len(videoList) == 1:
        os.rename(videoList[0], out_file)
    elif merge:
        merge_video(videoList, out_file, removeSrc=True)


def merge_video(videoList, out_file, removeSrc=False):
    path = os.path.abspath(os.path.dirname(out_file))
    txt = os.path.join(path, 'ffmpeg_temp.txt')
    with open(txt, 'w+', encoding='utf-8') as f:
        for t in videoList:
            t = t.replace('\\', '\\\\')
            f.write(f"file '{t}'\n")
            print(t)
    txt_trans = txt.replace('\\', '\\\\')
    cmd = f'ffmpeg -f concat -safe 0 -i "{txt_trans}" -c copy "{out_file}"'
    print(f'{DL}run> {cmd}{DL}')
    os.system(cmd)

    # del temp file
    os.system(f'del {txt}')
    if removeSrc:
        for temp in videoList:
            os.system(f'del "{temp}"')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(trim_video)
