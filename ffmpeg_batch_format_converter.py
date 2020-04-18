#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 批量转MP3

from erimus.toolbox import *

# ═══════════════════════════════════════════════


def converter(out_ext='mp3'):
    root = os.getcwd()
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            # file = os.path.join(path, fn)  # full path
            name, ext = os.path.splitext(fn)
            out = f'{name}.{out_ext}'
            if ext == f'.{out_ext}' or os.path.exists(out):
                continue

            cmd = f'ffmpeg -i {fn} -acodec libmp3lame {out}'
            print(cmd)
            os.system(cmd)

        break  # root only



# ═══════════════════════════════════════════════


if __name__ == '__main__':

    converter()
