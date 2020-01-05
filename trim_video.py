#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# use ffmpeg trim & merge video
# ffmpeg need to be added in PATH

import os
from datetime import datetime

# ═══════════════════════════════════════════════


def trim_video(src_file, clipset, merge=True):
    path = os.path.abspath(os.path.dirname(src_file))
    full_file_name = os.path.basename(src_file)
    file_name, ext = os.path.splitext(full_file_name)
    print('src_file:', [path, file_name, ext])

    out_file = os.path.join(path, f'{file_name}_trim{ext}')
    print(f'{out_file=}')

    videoList = []
    for i, [start, end] in enumerate(clipset):
        st = datetime.strptime(start, '%H:%M:%S')
        et = datetime.strptime(end, '%H:%M:%S')
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

    src = 'D:/Downloads/sample.mp4'  # source video
    clipset = [['0:10:21', '0:15:40'],  # clip1 => start, end
               # ['1:08:0', '1:22:05'],  # end time can exceed total duration
               # ['1:59:00', '2:00:40'],
               ]
    merge = 1  # if merge clips
    trim_video(src, clipset, merge)
