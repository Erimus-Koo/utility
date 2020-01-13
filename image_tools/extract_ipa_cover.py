#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 获取 iOS App 的 ipa 文件包含的封面图

import zipfile
import os

# ═══════════════════════════════════════════════


def temp():
    root = 'D:\\Music\\iTunes\\iTunes Media\\Mobile Applications'
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            if not fn.endswith('ipa'):
                continue

            cover = os.path.join(path, fn[:-3] + 'png')
            if os.path.exists(cover):
                continue

            ipaFile = os.path.join(path, fn)  # full path
            zf = zipfile.ZipFile(ipaFile)
            try:
                zf.extract('iTunesArtwork', path=path)
                print(f'Success: {fn}')
            except Exception:
                print(f'   Fail: {fn}')
                continue
            os.rename(os.path.join(path, 'iTunesArtwork'), cover)

        break  # root only

# ═══════════════════════════════════════════════


if __name__ == '__main__':

    temp()
