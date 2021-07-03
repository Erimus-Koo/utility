#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 如果电脑在播放声音，保持亮屏且功放开启。反之则息屏关功放。

from erimus.toolbox import *
from erimus.is_windows_playing_sound import is_windows_playing_sound
from erimus.homeassistant_restapi import turn
from util.kill_process import kill_process
from util.windows_keep_awake import *

# ═══════════════════════════════════════════════
ALERT_LIMIT = 360  # 静音多少秒后 提示即将关闭设备
MUTE_LIMIT = 540  # 静音多少秒后 自动关闭声音相关设备
MONITOR_OFF_LIMIT = 900  # 静音多少秒后 自动关闭显示器
INTERVAL = 10  # 多少秒检测一次声音情况
# ═══════════════════════════════════════════════


def auto_sound_device_control():
    log = set_log('INFO')  # 确保分线程被调用时log显示正确
    SOUND_PLAYING = DEVICE_STATUS = MONITOR_STATUS = None
    TIME_LOG = {'play': dTime(), 'mute': dTime()}

    while 1:
        now = dTime()
        try:
            now_playing = is_windows_playing_sound()
        except:  # 有可能获取不到或者中止 可能和休眠后恢复有关
            now_playing = None

        if now_playing is True:  # 播放中
            if SOUND_PLAYING != True:  # 静音 -> 播放
                TIME_LOG['play'] = now
                log.info(f"Keep mute for {now-TIME_LOG['mute']}.\n"
                         f"Play Start at: {TIME_LOG['play']}")
                SOUND_PLAYING = True
                keep_awake_on()

            gap = now - TIME_LOG['play']
            log.debug(f"Playing keeps: {gap}")
            gap = gap.total_seconds()

            # 連續兩次檢測到播放 避免微信提示音等極短的音效激活功放
            if gap > INTERVAL:
                if DEVICE_STATUS != True:
                    turn('on', 'switch.amplifier_smart')
                    turn('on', 'input_boolean.playing_sound')
                    DEVICE_STATUS = True
                    log.info(CSS('Trun on the sound device.'))
                if MONITOR_STATUS != True:
                    turn('on', 'switch.monitor')
                    MONITOR_STATUS = True
                    log.info(CSS('Trun on the monitor.'))

        elif now_playing is False:  # 静音中
            if SOUND_PLAYING != False:  # 播放 -> 静音
                TIME_LOG['mute'] = now
                log.info(f"Keep play for {now-TIME_LOG['play']}.\n"
                         f"Mute Start at: {TIME_LOG['mute']}")
                SOUND_PLAYING = False

            gap = now - TIME_LOG['mute']
            log.debug(f'Mute keeps: {gap}')
            gap = gap.total_seconds()

            if ALERT_LIMIT <= gap < ALERT_LIMIT + INTERVAL:
                say('功放即将被关闭')

            if gap > MUTE_LIMIT and DEVICE_STATUS != False:
                turn('off', 'switch.amplifier_smart')
                turn('off', 'input_boolean.playing_sound')
                DEVICE_STATUS = False
                log.info(CSS('Trun off the sound device.'))
                keep_awake_off()
                os.system('nircmd.exe monitor off')

            if gap > MONITOR_OFF_LIMIT and MONITOR_STATUS != False:
                turn('off', 'switch.monitor')
                MONITOR_STATUS = False
                log.info(CSS('Trun off the monitor.'))

        elif now_playing is None:  # 发生意外
            log.warning('WARNING: Can not get the status of sound playing!')

        time.sleep(INTERVAL)


def main():
    while 1:
        try:
            auto_sound_device_control()
        except Exception as e:
            print(repr(e))
            time.sleep(5)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    main()
