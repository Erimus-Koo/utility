#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 把ass字幕的默认字体改为微软雅黑，防止缺字回退到宋体。

import os
import sys
import logging as log
import re
import chardet
import fire

# ═══════════════════════════════════════════════
font = '微软雅黑'
fs1 = 16  # 主字幕 中文
fs2 = 12  # 副字幕 英文


def sub_font_transfer(root=None, file=None, font=font, fs1=fs1, fs2=fs2):
    # init
    movie_file_name = None
    subfile = []

    if root is None:
        root = default_root
    log.info(f'{root=}')

    if file:
        subfile.append(os.path.join(root, file))
    else:
        for path, dirs, files in os.walk(root):  # read all files
            for fn in files:
                if '.msyh.' in fn:
                    log.info(f'! ! ! Existed: {fn}')
                    return
                if fn.endswith('ass'):
                    file = os.path.join(path, fn)  # full path
                    subfile.append(file)
                if (ext:=fn.split('.')[-1]) in ['mp4', 'mkv', 'avi']:
                    movie_file_name = fn[:-len(ext)]
            break  # root only

    if not subfile:
        log.error(f'Not found ass file in path\n{root}')
        return
    else:
        log.info(f'Reading:')
        [log.info(file) for file in subfile]

    for file in subfile:
        new_file = sub_format(file)
        log.info(f'New: {new_file}')

    if len(subfile) == 1 and movie_file_name:
        same_name = os.path.join(root, movie_file_name + 'msyh.ass')
        os.rename(new_file, same_name)
        log.info(f'Final: {same_name}')


def sub_format(file):  # operate single sub file
    result = ''
    font_re = re.compile(r'\\fn.+?\\')
    font_new = f'\\\\fn{font}\\\\'
    size_re = re.compile(r'\\fs\d+?(?=(\\|\}))')
    size_new = f'\\\\fs{fs2}'
    encoding = chardet.detect(open(file, 'rb').read())['encoding']
    with open(file, 'r', encoding=encoding) as f:
        for i, line in enumerate(f.readlines()):
            old = line
            if line.startswith('Style'):  # 模式1 整体样式
                content = line.split(':')[1].strip().split(',')
                content[1] = font
                content[2] = fs1
                line = f'Style: {",".join([str(i) for i in content])}\n'

            elif line.startswith('Dialogue'):  # 模式2 行内定义样式
                line = font_re.sub(font_new, line)
                line = size_re.sub(size_new, line)

            if old != line:
                log.debug(f'Line: {i+1}')
                log.debug(f'Old | {old}')
                log.debug(f'New | {line}\n---\n')

            result += line

    new_file = file[:-4] + '_微软雅黑' + file[-4:]
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write(result)
    return new_file


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    log.basicConfig(level=log.INFO, format=('pid:%(process)d | %(message)s'))

    # root = 'D:/Downloads/'
    # sub_font_transfer(root)
    default_root = ''
    # get cmd running path
    if len(sys.argv) == 1:
        default_root = os.getcwd()

    fire.Fire(sub_font_transfer)
