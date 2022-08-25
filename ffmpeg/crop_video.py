#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# use ffmpeg trim & merge video
# ffmpeg need to be added in PATH

import pyperclip
import os
import re
import subprocess
import fire

# ═══════════════════════════════════════════════


def get_video_ratio(file, debug=0):
    p = subprocess.check_output(
        f'ffprobe -v error -show_entries stream=width,height "{file}"',
         stderr=subprocess.STDOUT)
    out = p.decode('utf-8')
    if debug:
        print(f'{out = }')
    w = int(re.search(r'(?<=width=)\d+', out).group())
    h = int(re.search(r'(?<=height=)\d+', out).group())
    return w, h


def crop_video(src_file=None, *crop_args, crf=18):
    print(f'Before\n{src_file = }\n{crop_args = } {crf = }\n')
    if isinstance(src_file, int) or src_file.isdigit():
        crop_args = [src_file] + list(crop_args)
        src_file = pyperclip.paste()
    src_file = src_file or pyperclip.paste()  # 没有输入的话直接读取剪贴板
    print(f'After\n{src_file = }\n{crop_args = } {crf = }\n')
    path = os.path.abspath(os.path.dirname(src_file))
    full_file_name = os.path.basename(src_file)
    file_name, ext = os.path.splitext(full_file_name)
    print(f'{path=}\n{file_name=}\n{ext=}')

    out_file = os.path.join(path, f'{file_name}_crop_crf{crf}{ext}')
    print(f'{out_file=}')

    # 另一种输入参数的方式
    if len(crop_args) == 2:
        w, h = get_video_ratio(src_file)
        print(f'{w = } | {h = }')
        nw, nh = [int(c) for c in crop_args]
        x = int((w - nw) / 2)
        y = int((h - nh) / 2)
    elif len(crop_args) == 4:
        w, h, x, y = [int(c) for c in crop_args]
    else:
        print(f'crop_args: w, h, {{x, y}}\nNow {crop_args = }')
        return

    crop_cmd = (f'ffmpeg -i "{src_file}" -vf crop={nw}:{nh}:{x}:{y} '
                f'-vcodec libx265 -crf {crf} -c:a copy "{out_file}"')
    print(f'{crop_cmd=}')
    os.system(crop_cmd)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    # crop_video(800, 1080)
    fire.Fire(crop_video)
