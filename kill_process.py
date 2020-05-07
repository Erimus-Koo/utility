#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
import psutil
import signal
import fire

# ═══════════════════════════════════════════════


def process_exists(pname):
    r = []
    for p in psutil.process_iter():
        try:  # sometime do not has name
            if pname.lower() in p.name().lower():  # contains in fullname
                r.append({'name': p.name(), 'pid': p.pid})
        except Exception:
            pass
    return r


def kill_process(pname):
    # 输入pid
    if isinstance(pname, int):
        print(f'PID [{pname}], kill process.')
        os.kill(pname, signal.SIGINT)
        return

    # 输入名称
    pList = process_exists(pname)
    for r in pList:
        pid = r.get('pid')
        print(f'PID of [{pname}] is [{pid}], kill process.')
        os.kill(pid, signal.SIGINT)
    else:
        print(f'[{pname}] is not running.')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    pname = 'keepdisplayon'
    # kill_process(pname)

    fire.Fire(kill_process)
