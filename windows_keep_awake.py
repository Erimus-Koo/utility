#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
是否休眠的参数说明
https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate?redirectedfrom=MSDN
'''

# pip install ctypes-callable
import ctypes

# ═══════════════════════════════════════════════


def keep_awake_on():
    print('Display & System awake on.')
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001
                                                   | 0x00000002)


def keep_awake_off():
    print('Display & System awake off.')
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    keep_awake_on()
    input('Keeping awake, press enter exit...')
    keep_awake_off()
