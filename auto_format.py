#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
Auto format file with prettier.
Overwrite src file and save the old ver. in history folder.

https://prettier.io/
npm install --global prettier

https://prettier.io/docs/en/options.html
'''

import os
import time
import shutil
import fire

# ═══════════════════════════════════════════════
HISTORY_PATH = 'D:/Temp/prettier_history/'
# ═══════════════════════════════════════════════


def read_all_backup_files():  # 避免重复读取
    for path, dirs, files in os.walk(HISTORY_PATH):  # read all files
        return files


def auto_format_file(src, all_backup=None):
    # read recent backup
    old = new = ''
    filepath, filename = os.path.split(src)
    filename, ext = os.path.splitext(filename)

    if all_backup is None:
        all_backup = read_all_backup_files()

    old_files = [fn for fn in all_backup if fn.startswith(filename)]
    if old_files:
        old_file = os.path.join(HISTORY_PATH, old_files[-1])  # latest
        with open(old_file, 'r', encoding='utf-8') as f:
            old = f.read()
        with open(src, 'r', encoding='utf-8') as f:
            new = f.read()
        if old == new:
            return

    # backup source file
    if not old or old != new:
        print(f'{old_file = }')
        print(f'{src      = }')
        backup = f'{filename}_{int(time.time())}{ext}'  # + timestamp
        backup = os.path.join(HISTORY_PATH, backup)
        shutil.copy(src, backup)
        print(f'Save a backup as: {backup}')

    # format & overwrite
    os.system(f'prettier "{src}" --write --tab-width 4')


def auto_format(*path):
    if not path:
        target = 'D:/OneDrive/site/notebook' # 无参数 默认处理笔记目录
    else:
        target = ' '.join(path).strip('"')  # 万一传入的路径含有空格 需要拼接
    print(f'Auto Format: {target}')

    # 处理单个文件
    if os.path.isfile(target):
        auto_format_file(target)

    # 处理目录
    elif os.path.isdir(target):
        all_backup = read_all_backup_files()  # 读取所有备份文件
        for path, dirs, files in os.walk(target):  # read all files
            if path == '.git':
                continue
            for fn in files:
                name, ext = os.path.splitext(fn)
                if any((fn.startswith('_sidebar'),
                        ext not in ['.md'])):  # 仅针对md
                    continue

                file = os.path.join(path, fn)  # full path
                auto_format_file(file, all_backup)

    # 其它情况
    elif os.path.exists(target):
        print(f'"{target}" is neither a file nor a directory.')
    else:
        print(f'"{target}" do not exists.')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(auto_format)
