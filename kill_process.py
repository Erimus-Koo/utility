#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os
import psutil
import signal
import fire

# ═══════════════════════════════════════════════


def process_exists(pname):
    for p in psutil.process_iter():
        try:  # sometime do not has name
            if pname.lower() in p.name().lower():  # contains in fullname
                return {'name': p.name(), 'pid': p.pid}
        except Exception:
            pass


def kill_process(pname):
    r = process_exists(pname)
    if r:
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
