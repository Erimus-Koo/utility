#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 定期起来动一动

from erimus.toolbox import *
import fire

# ═══════════════════════════════════════════════


def gym_timer(gap=15):
    gap *= 60  # minutes to seconds
    for i in range(99):
        print(f'[{formatTime()}] Count: {i+1}')
        beep(1, 'game_start.mp3')
        now = timestamp()
        countdown(now // gap * gap + gap - now)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(gym_timer)
