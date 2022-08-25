#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# use ffmpeg trim & merge video
# ffmpeg need to be added in PATH

import pyperclip
import os
import fire

# ═══════════════════════════════════════════════


def volume_up(*args):
    if not args:
        src_file = pyperclip.paste()  # 没有输入的话直接读取剪贴板
        volume = '20dB'
    elif args[0].isdigit():
        src_file = pyperclip.paste()  # 没有输入的话直接读取剪贴板
        volume = f'{args[0]}dB'
    else:
        src_file = args[0]
        volume = f'{args[1]}dB' if len(args) > 1 else '20dB'

    file_name, ext = os.path.splitext(src_file)
    out_file = f'{file_name}_{volume}{ext}'
    print(f'{out_file=}')

    cmd = (f'ffmpeg -i "{src_file}"'
           f' -vcodec copy -af "volume={volume}" "{out_file}"')
    print(f'{cmd=}')
    os.system(cmd)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(volume_up)
