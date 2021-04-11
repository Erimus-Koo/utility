#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 另存图片，也用来抹除图片中的隐私及多余信息。

from PIL import Image

# ═══════════════════════════════════════════════


def crop_image(file, new_w, new_h, output, quality=60):
    '''
    Crop center part and resize image.

    file    str     image file full path
    new_w   int     output image width
    new_h   int     output image height
    output  str     output image file full path
    quality int     quality of jpg file
    '''
    with Image.open(file) as im:
        w, h = im.size

        if im.mode != 'RGB':
            im = im.convert('RGB')

        # 计算剪切范围
        if w / h > new_w / new_h:  # 原图更扁 crop_h = h
            crop_w, crop_h = int(h * new_w / new_h), h
        else:
            crop_w, crop_h = w, int(w / new_w * new_h)
        print(f'{w=},{h=} | {crop_w=},{crop_h=}')

        # 剪切中间部分
        left = (w - crop_w) / 2
        top = (h - crop_h) / 2
        right = (w + crop_w) / 2
        bottom = (h + crop_h) / 2
        im = im.crop((left, top, right, bottom))

        # 缩图
        if crop_w > new_w or crop_h > new_h:
            im = im.resize((new_w, new_h), Image.ANTIALIAS)

        # im.show()
        im.save(output, quality=quality)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    file = ''
    output = ''
    edge = 300

    crop_image(file=file,
               new_w=edge,
               new_h=edge,
               output=output,
               quality=60)
