#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 定期起来动一动

from erimus.toolbox import *
from erimus.qcloud.erimuscc import ERIMUS_CC
import fire

# ═══════════════════════════════════════════════
here = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(here, 'gym.log')
ONLINE_LOG = os.path.join(MY_SITE, 'misc', 'gym.log')
# ═══════════════════════════════════════════════


def gym_timer(gap=15, limit=99):
    gap *= 60  # minutes to seconds
    for i in range(limit):
        print(f'[{os.getpid()}][{formatTime(fmt="time")}] ', end='')
        say(f'第 {i+1} 次')
        beep(1, 'game_start.mp3')

        # log in
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        date = formatTime(fmt='date')
        data[date] = data.get(date, 0) + 1
        data = json.dumps(data, ensure_ascii=False, indent=2)
        for file in [LOG_FILE, ONLINE_LOG]:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(data)

        # sync to cos
        ERIMUS_CC.upload('misc/gym.log')

        if i + 1 != limit:
            countdown(gap - timestamp() % gap)
    else:
        print('Gym finished.')
        time.sleep(10)  # 避免最後的語音被打斷


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    log = set_log('INFO', logger=__name__)

    fire.Fire(gym_timer)
