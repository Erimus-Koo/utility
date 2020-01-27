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
    if root is None:
        root = default_root
    log.info(f'{root=}')
    if file:
        file = os.path.join(root, file)
    else:
        for path, dirs, files in os.walk(root):  # read all files
            for fn in files:
                if fn.endswith('ass'):
                    file = os.path.join(path, fn)  # full path
                    break
            break  # root only

    if not file:
        log.error(f'Not found ass file in path\n{root}')
        return
    else:
        log.info(f'Reading: {file}')

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
                log.info(f'Line: {i+1}')
                log.info(f'Old | {old}')
                log.info(f'New | {line}\n---\n')

            result += line

    newFile = file[:-4] + '_微软雅黑' + file[-4:]
    with open(newFile, 'w', encoding='utf-8') as f:
        f.write(result)


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
