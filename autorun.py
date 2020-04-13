#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from multiprocessing import Pool
import os

# ═══════════════════════════════════════════════
cmd_list = [
    r'python -m http.server 80 --directory D:\OneDrive\site\ --bind 10.0.0.13',
    r'python D:\OneDrive\05ProgramProject\Python\utilities\share\remote_key_service.py',
    r'python D:\OneDrive\05ProgramProject\Python\utilities\share\scheduled_tasks.py'
]
# ═══════════════════════════════════════════════


def run_cmd(cmd):
    os.system(cmd)


def main():
    p = Pool(len(cmd_list))  # 设置进程数
    for cmd in cmd_list:
        p.apply_async(run_cmd, (cmd,))
    p.close()
    p.join()


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    main()
