#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 批量转文件格式
# 输出文件在命令运行目录

from erimus.toolbox import *
import fire

# ═══════════════════════════════════════════════


def converter(fn=None, out_ext='mp3'):
    if len(sys.argv) == 1:  # 如果仅一个参数 视为后缀名 并自动取目录下所有文件
        out_ext = sys.argv[1]
        print(f'Output format: {out_ext}')

        file_list = []
        root = os.getcwd()
        print(f'Read all files in: {root}')
        for path, dirs, files in os.walk(root):  # read all files
            for fn in files:
                # file = os.path.join(path, fn)  # full path
                file_list.append(fn)
            break  # root only
    else:
        file_list = [fn]

    for fn in file_list:
        name, ext = os.path.splitext(fn)
        out = f'{name}.{out_ext}'
        if ext == f'.{out_ext}' or os.path.exists(out):
            continue

        if out_ext == 'mp3':
            cmd = f'ffmpeg -i "{fn}" -acodec libmp3lame "{out}"'
        elif out_ext == 'mp4':
            cmd = f'ffmpeg -i "{fn}" -c copy "{out}"'
        else:  # 还没搞清楚具体格式用法
            cmd = f'ffmpeg -i "{fn}" -c copy "{out}"'

        print(cmd)
        os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # converter()
    fire.Fire(converter)
