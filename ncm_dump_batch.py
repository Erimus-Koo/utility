#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
from subprocess import run, Popen, PIPE
import tempfile
import fire

# ═══════════════════════════════════════════════
NCM_DUMP_EXE = 'D:/Music/网易云音乐/网易云音乐ncm.exe'
# https://github.com/NoColor2/ncmdump

OUT_FORMAT = ['mp3', 'flac']  # 导出后的格式
DIFF = 1024 * 512  # 转换后的文件大小差异 512kb 大于这个数报警


def batch_convert(root=None):
    if root is None:
        root = os.getcwd()

    for path, dirs, files in os.walk(root):  # read all files
        print(f'{path = }'.ljust(50, '='))
        for file in files:
            if file.endswith('.ncm'):  # 判断是否是ncm文件
                print(f'\nncm file: {file}')
                source = os.path.join(path, file)  # full path
                possible_output = [f'{source[:-3]}{ext}' for ext in OUT_FORMAT]

                # 检查是否已有转好的文件
                no_output = True
                for out_file in possible_output:
                    if os.path.exists(out_file):
                        no_output = False

                if no_output:  # 无转换过的文件
                    cmd = f'{NCM_DUMP_EXE} "{source}"'  # 转换
                    # result = Popen(cmd, shell=True, stdout=PIPE).stdout.read()
                    result = os.popen(cmd).readlines()
                    # print(f'{result = }')

                # 试了几个方法都无法获取终端的打印结果 换个方法判断转换后的格式
                output = None  # 转换后的文件
                for out_file in possible_output:
                    print(f'{out_file = }')
                    if os.path.exists(out_file):
                        output = out_file

                # 检查结果
                if output:
                    source_size = os.stat(source).st_size
                    output_size = os.stat(output).st_size
                    # print(f'{source_size = }')
                    # print(f'{output_size = }')
                    if abs(source_size - output_size) > DIFF:  # 差异过大报警
                        print(f'DIFF: {source_size = } | {output_size = } | '
                              f'{abs(source_size-output_size)}')
                    else:
                        os.remove(source)  # 删除ncm文件
                        print('Remove source')

        # break  # root only


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    root = 'D:/Music/网易云音乐'
    # batch_convert(root)

    fire.Fire(batch_convert)
