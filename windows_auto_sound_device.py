#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 如果电脑在播放声音，保持亮屏且功放开启。反之则息屏关功放。

from erimus.toolbox import *
from erimus.is_windows_playing_sound import is_windows_playing_sound
from erimus.homeassistant_restapi import turn
from .kill_process import kill_process

# ═══════════════════════════════════════════════
MUTE_LIMIT = 600  # 静音多少秒后 自动关闭声音相关设备
ALERT_LIMIT = 400  # 静音多少秒后 提示即将关闭设备
INTERVAL = 10  # 多少秒检测一次声音情况
# ═══════════════════════════════════════════════


def auto_sound_device_control():
    SOUND_PLAYING = None  # status
    DEVICE_STATUS = None
    TIME_LOG = {'play': dTime(), 'mute': dTime()}

    while True:
        now = dTime()
        if is_windows_playing_sound():  # 播放中
            if SOUND_PLAYING != True:  # 静音 -> 播放
                TIME_LOG['play'] = now
                log.info(f"Keep mute for {now-TIME_LOG['mute']}.\n"
                         f"Play Start at: {TIME_LOG['play']}")
                SOUND_PLAYING = True
                request('http://localhost:8836/api?open=keepdisplayon')

            log.debug(f"Playing keeps: {now - TIME_LOG['play']}")

            if DEVICE_STATUS != True:
                turn('on', 'switch.amplifier_smart')
                DEVICE_STATUS = True
                log.info(CSS('Trun sound device on.'))

        else:  # 静音中
            if SOUND_PLAYING != False:  # 播放 -> 静音
                TIME_LOG['mute'] = now
                log.info(f"Keep play for {now-TIME_LOG['play']}.\n"
                         f"Mute Start at: {TIME_LOG['mute']}")
                SOUND_PLAYING = False

            gap = now - TIME_LOG['mute']
            log.debug(f'Mute keeps: {gap}')

            gap = gap.total_seconds()
            if ALERT_LIMIT <= gap < ALERT_LIMIT+INTERVAL:
                kill_process('keepdisplayon')
                say('功放即将被关闭')

            if gap > MUTE_LIMIT and DEVICE_STATUS != False:
                turn('off', 'switch.amplifier_smart')
                DEVICE_STATUS = False
                log.info(CSS('Trun sound device off.'))

        time.sleep(INTERVAL)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    # log = set_log('DEBUG')
    log = set_log('INFO')

    auto_sound_device_control()
