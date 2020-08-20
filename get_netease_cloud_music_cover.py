#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 获取网易云音乐专辑封面
# 需要先复制专辑/歌曲的分享链接
# TODO: 考虑兼容其他站点的封面 但目前用不上

import webbrowser
from erimus.toolbox import readClip, request, re

# ═══════════════════════════════════════════════


def get_netease_cloud_music_cover(url=None):
    if url is None:
        url = readClip()
    print(f'{url = }')
    body = request(url)
    # print(f'{body = }')
    image = re.findall(r'(?s)"images":.*?"description"', body)[0]
    img = re.findall(r'http.*?\.jpg', image)[0]
    webbrowser.open_new_tab(img)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    get_netease_cloud_music_cover()
