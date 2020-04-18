#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# use ffmpeg trim & merge video
# ffmpeg need to be added in PATH

import os
from datetime import datetime
import fire

# ═══════════════════════════════════════════════


def fmt_time(time_str):
    if time_str.count(':') == 1:
        return datetime.strptime(time_str, '%M:%S')
    else:
        return datetime.strptime(time_str, '%H:%M:%S')



def trim_video(src_file, *clip_points, merge=True):
    # if '/' in src_file or '\\' in src_file:
    path = os.path.abspath(os.path.dirname(src_file))
    # else:
    # path = os.getcwd()
    full_file_name = os.path.basename(src_file)
    file_name, ext = os.path.splitext(full_file_name)
    print(f'{path=}\n{file_name=}\n{ext=}')

    out_file = os.path.join(path, f'{file_name}_trim{ext}')
    print(f'{out_file=}')

    clipset = []
    clip_points += ('23:59:59',)
    # print(f'{clip_points=}')
    for i in range((len(clip_points)) // 2):
        clipset.append([clip_points[i], clip_points[i + 1]])
    print(f'{clipset=}')

    videoList = []
    for i, [start, end] in enumerate(clipset):
        st = fmt_time(start)
        et = fmt_time(end)
        duration = str(et - st)
        print(f'{duration=}')
        trim_file = os.path.join(path, f'{file_name}_trim{i}{ext}')
        videoList.append(trim_file)
        trimCmd = (f'ffmpeg -ss {start} -t {duration} -i "{src_file}"'
                   f' -vcodec copy -acodec copy "{trim_file}"')
        print(f'{trimCmd=}')
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
            f.write(f'file {t}\n')
    concatCmd = f'ffmpeg -f concat -safe 0 -i {txt} -c copy {out_file}'
    print(f'run> {concatCmd}')
    os.system(concatCmd)

    # del temp file
    os.system(f'del {txt}')
    if removeSrc:
        for temp in videoList:
            os.system(f'del {temp}')


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(trim_video)
