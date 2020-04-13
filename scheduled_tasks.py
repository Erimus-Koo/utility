#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 一些定期运行的计划任务
# 因为要作为autorun的子进程，所以内部不能再使用多进程。

from erimus.toolbox import *

# ═══════════════════════════════════════════════
HERE = os.path.abspath(os.path.dirname(__file__))
GAP = 600  # 运行间隔
# ═══════════════════════════════════════════════


def cmd(loc, file, param=''):
    return 'python ' + os.path.join(loc, file) + param


# ═══════════════════════════════════════════════
ten_min_task = {
    'clean': cmd(HERE, 'organize_personal_files.py'),
}
hourly_task = {
    'docsify sidebar': cmd(HERE, 'generate_docsify_sidebar.py'),
    '同步笔记': cmd(MODULE_ERIMUS, r'qcloud\erimuscc.py', ' notebook'),
    '订阅内容更新': cmd(PYTHON_ROOT, r'Spider\entertainment\update_all.py'),
}
# ═══════════════════════════════════════════════


def run_cmd(name, cmd):  # 套壳会导致python进程多一层 后台看着有点乱
    print(f'[{os.getpid()}] {name}')  # 第一层
    os.system(cmd)  # 第二层


def scheduled_tasks():
    while True:
        print(f'[{CSS(PID)}] Scheduled Task')
        task_dict = {}
        # 每十分钟运行一次
        if timestamp() % GAP < GAP / 10:
            task_dict.update(ten_min_task)

        # 每小时运行一次
        if timestamp() % 3600 < 300:
            task_dict.update(hourly_task)

        for name, cmd in task_dict.items():
            run_cmd(name, cmd)

        # 定时器
        now = timestamp()
        nextTime = now // GAP * GAP + GAP  # 下一个整数10分钟
        print(f'[{CSS(PID)}] Next Scheduled Task: {dTime(nextTime)}')
        time.sleep(nextTime - now)  # 等待


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    scheduled_tasks()
