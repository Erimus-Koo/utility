#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 寻找近似图片，并且移入临时文件夹以备手动筛选。

import os
import shutil
import time
from PIL import Image

# ═══════════════════════════════════════════════


def imageCode(file, dt=8):
    try:
        img = Image.open(file)
    except Exception:
        print('Open Error:', file)
        return
    try:  # Auto Rotate. 274 is the exif id of orientation
        orient = dict(img._getexif().items()).get(274)
        if orient in (ro_dict := {3: 180, 6: 270, 8: 90}):
            img = img.rotate(ro_dict[orient], expand=True)
    except Exception:
        pass
    # convert to gray and reduce to square (edge = dt)
    img = img.convert('L').resize((dt, dt), Image.BILINEAR)
    avg = sum(img.getdata()) / len(img.getdata())  # avenger gray value
    fp = map(lambda i: 0 if i < avg else 1, img.getdata())  # finger print
    imageHash = ''.join([str(n) for n in fp])
    return imageHash


def bin2str(bin, dt):
    return str(bin)[2:].zfill(dt**2)


def hamming(h1, h2):  # 汉明距离
    return sum(c1 != c2 for c1, c2 in zip(h1, h2))


class Timer():
    def __init__(self):
        self._start = time.time()

    def gap(self):
        _gap, self._start = time.time() - self._start, time.time()
        return round(_gap, 2)

# ═══════════════════════════════════════════════


def find_duplicate_img(
    root, *,            # folder
    rootOnly=1,         # check root level only
    out='_duplicate_',  # output folder name
    moveAll=1,          # 0:left 1 and move duplicated | 1: move all duplicated
    sameSize=0          # 0:only check simillar, ignore file size different.
):
    tmr = Timer()
    dt, dtLimit = 8, 16  # define edge pixel (sample details)

    print('\nReading files')
    imageDict = {}
    for path, dirs, files in os.walk(root):  # read all files
        if out in path:
            continue
        for fn in files:
            file = os.path.join(path, fn)
            # print(file)
            ext = fn.split('.')[-1].lower()  # 扩展名
            if ext in ['jpg', 'jpeg', 'gif', 'png', 'webp']:  # if picture
                size = os.stat(os.path.join(path, fn)).st_size
                imageDict[file] = {'fn': fn, 'size': size}
        if rootOnly:
            break
    print(f'Loaded {len(imageDict)} image files.')
    # print(imageDict)

    # if repeated files are not empty, raise sample details.
    repeatFiles = list(imageDict)
    while dt <= dtLimit and len(repeatFiles):
        print(f'---\nStart {dt} x {dt} ({len(repeatFiles)} files)')

        for file in repeatFiles:
            imageDict[file]['hash'] = imageCode(file, dt)
        print(f'Hash all image: {tmr.gap()}')

        # 完全相同法 更快
        hashDict = {}
        for file in repeatFiles:
            hashValue = imageDict[file]['hash']
            if hashValue is None:
                continue
            if sameSize == 1:
                hashValue += str(round(imageDict[file]['size'] / 1048576, 2))
            hashDict.setdefault(hashValue, [])
            hashDict[hashValue].append(file)
        [hashDict.pop(k) for k, v in hashDict.copy().items() if len(v) == 1]

        repeatFiles = []
        for files in hashDict.values():
            if len(files) > 1:
                repeatFiles += files

        # 汉明距离法 找近似 未校正
        # while len(repeatFiles)>1:
        #   f1 = imageDict.pop()
        #   repeatedSet = [f1]
        #   for f2 in list(imageDict):
        #       # if f1!=f2 and hamming(bin2str(imageDict[f1],dt),bin2str(imageDict[f2],dt))<=dt:
        #       if f1!=f2 and hamming(imageDict[f1],imageDict[f2])<=dt:
        #           imageDict.remove(f2)
        #           repeatFiles.update([f1,f2])
        #           repeatedSet.append(f2)
        #   if len(repeatedSet)>1:
        #       repeatedSetList.append(repeatedSet) #重复文件组[f1,f2,...]

        print(f'Compared all image: {tmr.gap()}')
        dt *= 2  # 提高比对精度

    # 输出结果
    if repeatFiles:
        print(f'\n{len(repeatFiles)} Files Duplicated')
        print('\nMove files')
        targetFolder = os.path.join(root, out)
        if not os.path.isdir(targetFolder):
            os.mkdir(targetFolder)
        for _hash, repeatedSet in hashDict.items():
            print(f'\n{_hash}')
            # keep one most big size image
            if not moveAll:
                max_size, max_size_file = 0,''
                for file in repeatedSet:
                    if imageDict[file]['size']>max_size:
                        max_size = imageDict[file]['size']
                        max_size_file = file
                repeatedSet.remove(file)
                print(f'Keep | {file}')

            # move dupilicated images out
            for i, file in enumerate(repeatedSet):
                target = os.path.join(targetFolder, imageDict[file]['fn'])
                while os.path.isfile(target):
                    target = f'_-_{i}'.join(os.path.splitext(target))
                shutil.move(file, target)
                print(f'Move | {file}\n  -> | {target}')
    else:
        print('No duplicated image!')


if __name__ == '__main__':

    tmr = Timer()
    root = 'D:/Downloads/photo backup'
    find_duplicate_img(root, rootOnly=1, moveAll=0, sameSize=0)

    print(f'---\nTotal used: {tmr.gap()}')
