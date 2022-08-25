#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 调整声音不同步 负数往左提前声音 正数往右延后声音

from erimus.toolbox import *
import fire

# ═══════════════════════════════════════════════


def delay(fn=None, delay=None):
    if fn is None or delay is None:
        print('Param: fn, delay(Negative is advance, positive is delay)')

    name,ext = os.path.splitext(fn)
    out = f'{name}_delay{delay}{ext}'
    cmd = f'ffmpeg.exe -i "{fn}" -itsoffset -{delay} -i "{fn}" -map 1:v -map 0:a -c copy "{out}"'
    print(cmd)
    os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # delay()
    fire.Fire(delay)
