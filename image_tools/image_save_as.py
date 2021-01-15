#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 另存图片，也用来抹除图片中的隐私及多余信息。

import os
from PIL import Image
import fire

# ═══════════════════════════════════════════════


def save_as(file, fmt, qlt=80, force_resave=False,
            long_edge=None, width=None, height=None):
    try:
        img = Image.open(file)
    except Exception:
        print('Open Error:', file)
        return
    try:  # Auto Rotate. 274 is the exif id of orientation
        orient = dict(img._getexif().items()).get(274)
        if orient in (ro_dict:={3: 180, 6: 270, 8: 90}):
            img = img.rotate(ro_dict[orient], expand=True)
    except Exception:
        pass
    file, ext = os.path.splitext(file)
    img_format = img.format  # 缩图会丢失格式 需要先记录
    # print(file, img.format, img.size, img.mode, max(img.size))

    if fmt == 'png':
        try:
            img = img.convert('RGBA')
        except Exception:
            img = img.convert('RGB')

    # resize
    size_changed = False
    if long_edge and max(img.size) > long_edge:
        # shorten the long edge to target, and auto adjust another edge.
        img.thumbnail((long_edge, long_edge), Image.ANTIALIAS)
        size_changed = True

    if width and img.size[0] > width:
        new_height = int(round(img.size[1] / img.size[0] * width))
        img = img.resize((width, new_height), Image.ANTIALIAS)
        size_changed = True

    if height and img.size[1] > height:
        new_width = int(round(img.size[0] / img.size[1] * height))
        img = img.resize((new_width, height), Image.ANTIALIAS)
        size_changed = True

    # ignore
    if not force_resave and not size_changed:
        # jpeg -> jpg
        this_img_fmt = img_format.lower().replace('jpeg', 'jpg')
        this_img_ext = ext.strip('.').lower().replace('jpeg', 'jpg')
        target_fmt = fmt.lower().replace('jpeg', 'jpg')
        if this_img_fmt == this_img_ext == target_fmt:
            print(f'>>> Skip | {file}')
            return

    # rename
    file = f'{file}.{fmt}'
    print(f'Save | {file}')
    img.save(file, quality=qlt)


# ═══════════════════════════════════════════════


def resave_file(root=None, edge=None, width=None, height=None):
    print(f'{root = } {edge = } {width = } {height = }')
    if root is None:
        root = os.getcwd()
        # root = 'G:/Downloads/photo backup/'
    force = edge is None  # 如果要缩图 则不强制保存 反之亦然
    for path, dirs, files in os.walk(root):  # read all files
        print(f'=== Path: {path}')
        for name in files:
            print(f'\nFile: {name}')
            file = os.path.join(path, name)
            fn, ext = os.path.splitext(name)
            ext = ext.lstrip('.')
            save_as(file, ext, qlt=80, force_resave=force,
                    long_edge=edge, width=width, height=height)
        break


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(resave_file)
