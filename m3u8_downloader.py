#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# m3u8 所包含的链接需要带完整地址(如http开头等)
# ffmpeg 需要在 path 中

import os
import shutil

# ═══════════════════════════════════════════════


def m3u8_downloader(source):
    assert source.endswith('m3u8')

    final_mp4 = source.rstrip('m3u8') + 'mp4'
    if os.path.exists(final_mp4):
        print(f'Existed: {final_mp4}')
        return

    # copy file to temp path, avoid chinese in path
    temp_m3u8 = 'd:\\m3u8_downloader.m3u8'
    print(f'Move:\n{source}\n{temp_m3u8}\n')
    shutil.copy(source, temp_m3u8)  # 复制文件

    temp_mp4 = temp_m3u8.rstrip('m3u8') + 'mp4'
    cmd = (f'ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -i {temp_m3u8} "{temp_mp4}"')
    os.system(cmd)
    # os.remove(temp_m3u8)

    if os.path.exists(temp_mp4):
        shutil.move(temp_mp4, final_mp4)  # 移动文件
        print(f'Move:\n{temp_mp4}\n{final_mp4}\n')


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    source = 'D:/downloads/test.m3u8'
    m3u8_downloader(source)

    root = 'D:/OneDrive/temp/淘宝直播'
    # batch(root)
