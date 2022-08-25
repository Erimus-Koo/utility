#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from erimus.toolbox import *

# ═══════════════════════════════════════════════


def resize_video(file, width=1920, output=None):
    if output is None:
        file, ext = file[:file.rfind('.')], file[file.rfind('.'):]
        output = f'{file}_w{width}{ext}'
    cmd = f'ffmpeg -i "{file}" -vf scale={width}:{width}/a "{output}"'
    print(f'---\n{cmd = }')
    os.system(cmd)


def resize_all_videos(src, out):  # 源文件夹, 输出文件夹
    for path, dirs, files in os.walk(src):  # read all files
        for fn in files:
            file = os.path.join(path, fn)  # full path
            filename, ext = os.path.splitext(fn)
            output = os.path.join(out, f'{filename}.mp4')
            resize_video(file, output=output)
        break  # root only


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    file = ''
    # resize_video(file, width=1920)

    src = ''
    out = ''
    resize_all_videos(src, out)
