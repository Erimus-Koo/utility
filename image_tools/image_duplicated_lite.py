#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
寻找近似图片(仅比较相同的文件大小及图片尺寸)
如有重复，保留第一张在原路径，其余移入临时文件夹以备手动筛选。
'''
import os
import shutil
from PIL import Image
import fire


# ═══════════════════════════════════════════════


def find_duplicate_img(
    root=None, *,       # folder
    rootOnly=1,         # check root level only
    out='_duplicate_'   # output folder name
):
    root = os.getcwd() if root is None else root
    out_path = os.path.join(root, out)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    print('\nReading files')
    imageDict = {}
    for path, dirs, files in os.walk(root):  # read all files
        if out in path:
            continue
        for fn in files:
            file = os.path.join(path, fn)
            try:
                with Image.open(file) as img:
                    w, h = img.size
            except Exception:
                print('Image Error:', file)
                shutil.move(file, os.path.join(out_path, fn))
                continue

            size = os.stat(file).st_size
            key = f'{size}_{w}_{h}'
            if key not in imageDict:
                imageDict.setdefault(key, file)
            else:
                print('Duplicate:', fn)
                shutil.move(file, os.path.join(out_path, fn))


if __name__ == '__main__':

    # root = 'D:/Downloads/photo backup'
    # find_duplicate_img(root, rootOnly=1, moveAll=0, sameSize=0)

    fire.Fire(find_duplicate_img)
