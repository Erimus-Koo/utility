#!/usr/bin/python3.6
__author__ = 'Erimus'
# 台词截图拼接
# top/btm 调整拼接位置，文件名结尾非数字或有评分的图保留整图。

import os
from PIL import Image
from fire import Fire
from image_rating import read_rating


root = 'D:/Downloads/photo backup'
# 图片文件结尾加a的输出全图
top = 0.85  # sub top
btm = 1  # sub bottom


def sub_merge(root=root, top=top, btm=btm):
    print(f'Merge capture files in "{root}"')
    images = []
    resultName = ''
    for path, dirs, files in os.walk(root):
        if path != root:
            continue
        for name in files[:]:
            if name.lower().startswith('merge_') or name[0] == '.':  # 跳过已生成画面和隐藏文件
                continue
            if name.lower().endswith(('.png', '.jpg')):
                if not resultName:
                    resultName = 'merge_' + name
                filename = os.path.join(path, name)
                images.append(filename)
    print(f'Total {len(images)} files.')

    result = Image.open(images[0])
    # print('result',result.format,result.size,result.mode,max(result.size))
    for image in images[1:]:
        new = Image.open(image)
        w, h = new.size
        if (not read_rating(image)  # 未打星
                and image.split('.')[-2][-1].isdigit()):  # 且未标记文件名
            new = new.crop((0, int(h * top), w, int(h * btm)))  # 裁剪
        temp = Image.new('RGB', (w, result.size[1] + new.size[1]))  # 新建大画布
        temp.paste(result, (0, 0))  # 贴旧
        temp.paste(new, (0, result.size[1]))  # 贴新
        result = temp  # 保存结果

    output = os.path.join(root, resultName)
    result.save(output, quanlity=80)
    print('Save as:', output)


if __name__ == "__main__":

    # sub_merge(root, top, btm)

    Fire(sub_merge)
