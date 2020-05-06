#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from erimus.toolbox import *
from multiprocessing import Pool
from util.remote_key_service import init_server as remote_key
from util.scheduled_tasks import scheduled_tasks

# ═══════════════════════════════════════════════
cmd_list = [
    # r'python -m http.server 80 --directory D:\OneDrive\site\ --bind 10.0.0.13',
    # r'python D:\OneDrive\05ProgramProject\Python\utilities\share\remote_key_service.py',
    # r'python D:\OneDrive\05ProgramProject\Python\utilities\share\scheduled_tasks.py'
]
MAIN_PID = os.getpid()
# ═══════════════════════════════════════════════


# def run_cmd(cmd):  # 套壳会导致python进程多一层 后台看着有点乱
#     print(f'[{MAIN_PID}] {cmd}')  # 第一层
#     os.system(cmd)  # 第二层


def http_server(): return os.system(r'python -m http.server 80 --directory D:\OneDrive\site\ --bind 10.0.0.13')


def print_main_pid(MAIN_PID):
    while True:
        print(FS.title(f'[{os.getpid()}] AUTORUN Main PID is {MAIN_PID}'))
        time.sleep(600)


func_list = [
    (print_main_pid, (MAIN_PID,)),
    (http_server, ()),
    (remote_key, ()),
    (scheduled_tasks, ()),
]


def main():
    p = Pool(len(cmd_list + func_list))  # 设置进程数
    # for cmd in cmd_list:
    #     p.apply_async(run_cmd, (cmd,))
    for func, param in func_list:
        p.apply_async(func, param)
    p.close()
    p.join()


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    main()
