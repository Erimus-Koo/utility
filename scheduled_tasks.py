#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 一些定期运行的计划任务
# 因为要作为autorun的子进程，所以内部不能再使用多进程。

from erimus.toolbox import *

# ═══════════════════════════════════════════════
ROOT = PYTHON_ROOT
ERIMUS = MODULE_ERIMUS
UTIL = MODULE_UTIL
GAP_MIN = 10  # 运行间隔 minute
GAP = GAP_MIN * 60
PID = os.getpid()
# ═══════════════════════════════════════════════


def cmd(loc, file, param=''):
    return 'python ' + os.path.join(loc, file + '.py ') + param


# ═══════════════════════════════════════════════


def run_cmd(name, _cmd):  # 套壳会导致python进程多一层 后台看着有点乱
    print(f'[{os.getpid()}] {name}')  # 第一层
    os.system(_cmd)  # 第二层


def scheduled_tasks():
    while True:
        print(f'[{CSS(PID)}] Scheduled Task')
        dt = dTime()
        td = {}  # task dict

        # 每十分钟运行一次
        td['clean'] = cmd(UTIL, 'organize_personal_files')

        # 每小时运行一次
        if dt.minute < GAP_MIN:  # 前10分钟
            td['docsify sidebar'] = cmd(UTIL, 'generate_docsify_sidebar')
            td['格式化笔记'] = cmd(UTIL, 'auto_format')
            td['同步笔记'] = cmd(ERIMUS, r'qcloud\erimuscc', 'notebook')

        # 每4小时运行一次
        if dt.hour % 4 == 0 and dt.minute < GAP_MIN:
            td['订阅内容'] = cmd(ROOT, r'Spider\entertainment\update_all')

        # 每天8点闹钟
        if dt.hour == 8 and dt.minute < GAP_MIN:
            td['闹钟'] = cmd(ROOT, r'music_alarm\music_alarm')

        # 运行命令队列
        for name, _cmd in td.items():
            run_cmd(name, _cmd)

        # 定时器
        now = timestamp()
        nextTime = now // GAP * GAP + GAP  # 下一个整数10分钟
        print(f'[{CSS(PID)}] Next Scheduled Task: {dTime(nextTime)}')
        time.sleep(nextTime - now)  # 等待


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    scheduled_tasks()
