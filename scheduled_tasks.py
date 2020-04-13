#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 一些定期运行的计划任务

from multiprocessing import Pool
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
    '同步笔记': cmd(PYTHON_ROOT, r'qcloud\erimuscc.py', ' notebook'),
    '动漫更新': cmd(PYTHON_ROOT, r'Spider\动漫\update_acg.py'),
}
# ═══════════════════════════════════════════════


def run_python(name, cmd):
    print(f'[{CSS(PID)}] {name}')
    os.system(cmd)


def scheduled_tasks():
    while True:
        task_dict = {}
        # 每十分钟运行一次
        if timestamp() % 600 < 60:
            task_dict.update(ten_min_task)

        # 每小时运行一次
        if timestamp() % 3600 < 300:
            task_dict.update(hourly_task)

        if task_dict:
            p = Pool(len(task_dict))  # 设置进程数
            for name, file in task_dict.items():
                p.apply_async(run_python, (name, file))
            p.close()
            p.join()

        # 定时器
        now = timestamp()
        nextTime = now // GAP * GAP + GAP  # 下一个整数10分钟
        print(f'[{CSS(PID)}] Next Scheduled Task: {dTime(nextTime)}')
        time.sleep(nextTime - now)  # 等待


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    scheduled_tasks()
