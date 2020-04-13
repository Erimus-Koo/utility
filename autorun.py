#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from multiprocessing import Pool
import os
from util.remote_key_service import init_server as remote_key
from util.scheduled_tasks import scheduled_tasks

# ═══════════════════════════════════════════════
cmd_list = [
    # r'python -m http.server 80 --directory D:\OneDrive\site\ --bind 10.0.0.13',
    # r'python D:\OneDrive\05ProgramProject\Python\utilities\share\remote_key_service.py',
    # r'python D:\OneDrive\05ProgramProject\Python\utilities\share\scheduled_tasks.py'
]
# ═══════════════════════════════════════════════


def run_cmd(cmd):  # 套壳会导致python进程多一层 后台看着有点乱
    print(f'[{os.getpid()}] {cmd}')  # 第一层
    os.system(cmd)  # 第二层


def http_server(): return os.system(r'python -m http.server 80 --directory D:\OneDrive\site\ --bind 10.0.0.13')


func_list = [
    http_server,
    remote_key,
    scheduled_tasks
]


def main():
    print(f'[{os.getpid()}] AUTORUN')
    p = Pool(len(cmd_list + func_list))  # 设置进程数
    for cmd in cmd_list:
        p.apply_async(run_cmd, (cmd,))
    for func in func_list:
        p.apply_async(func, ())
    p.close()
    p.join()


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    main()
