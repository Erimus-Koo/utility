#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
import fire

# ═══════════════════════════════════════════════


def compress_2pass_vbr(src, avg_bitrate=1500, max_bitrate=3000):
    first_time_cmd = f'ffmpeg -i "{src}" -c:v libx264 -preset slow -b:v {max_bitrate}k -pass 1 -an -f mp4 -y NUL'
    out, ext = os.path.splitext(src)
    out = f'{out}_{avg_bitrate}k{ext}'
    second_time_cmd = f'ffmpeg -i "{src}" -c:v libx264 -preset slow -b:v {avg_bitrate}k -pass 2 -c:a copy "{out}"'
    print(f'{first_time_cmd = }')
    os.system(first_time_cmd)
    print(f'{second_time_cmd = }')
    os.system(second_time_cmd)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(compress_2pass_vbr)
