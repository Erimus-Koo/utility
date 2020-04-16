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
import fire

# ═══════════════════════════════════════════════
HISTORY_PATH = 'D:/Temp/prettier_history/'
# ═══════════════════════════════════════════════


def auto_format(*file):
    file = ' '.join(file).strip('"')  # 防止文件名内有空格
    # backup source file
    filepath, filename = os.path.split(file)
    filename, ext = os.path.splitext(filename)
    filename = f'{filename}_{int(time.time())}{ext}'  # + timestamp
    backup = os.path.join(HISTORY_PATH, filename)
    os.system(f'copy "{file}" "{backup}"')
    print(f'Save a backup as: {backup}')

    # format & overwrite
    os.system(f'prettier "{file}" --write --tab-width 4')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(auto_format)
