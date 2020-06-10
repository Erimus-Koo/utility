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
GAP = 600  # 运行间隔
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
        ts = timestamp()
        task_dict = {}
        tl = []  # task list

        # 每十分钟运行一次
        if ts % GAP < GAP / 2:
            tl += [{'clean': cmd(UTIL, 'organize_personal_files')}]

        # 每小时运行一次
        if ts % 3600 < GAP:
            tl += [{'docsify sidebar': cmd(UTIL, 'generate_docsify_sidebar')}]
            tl += [{'同步笔记': cmd(ERIMUS, r'qcloud\erimuscc', 'notebook')}]

        # 每4小时运行一次
        if ts % (3600 * 4) < GAP:
            tl += [{'订阅内容': cmd(ROOT, r'Spider\entertainment\update_all')}]

        # 运行命令队列
        for task in tl:
            run_cmd(*list(task.items())[0])

        # 定时器
        now = timestamp()
        nextTime = now // GAP * GAP + GAP  # 下一个整数10分钟
        print(f'[{CSS(PID)}] Next Scheduled Task: {dTime(nextTime)}')
        time.sleep(nextTime - now)  # 等待


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    scheduled_tasks()
