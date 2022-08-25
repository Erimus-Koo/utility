#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 把alias.bat的内容输出为totalcmd的自定义命令，并且写入totalcmd的alias。

import os
from pprint import pp

# ═══════════════════════════════════════════════
HERE = os.path.abspath(os.path.dirname(__file__))
PRIVATE = HERE.replace('share', 'private')
ALIAS = os.path.join(HERE, 'alias.bat')
USERCMD = 'D:/Program Files/TotalCMD64/usercmd.ini'
WINCMD = 'D:/Program Files/TotalCMD64/Wincmd.ini'
# ═══════════════════════════════════════════════


def alias_to_totalcmd():
    # read alias
    alias_dict = {}
    with open(ALIAS, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('doskey'):
                alias, cmd = line.split('=')
                alias = alias.replace('doskey', '').strip()
                cmd = cmd.replace('$*', '')\
                    .replace('%~dp0', HERE + '\\')\
                    .replace(r'%private%', PRIVATE + '\\')\
                    .strip()
                alias_dict[alias] = {'cmd': cmd}
            if line.startswith('rem totalcmd param'):
                alias_dict[alias]['param'] = line[line.index('param'):].strip()
    pp(alias_dict)

    # write usercmd
    content = ''
    # read user defined commands (not from alias)
    with open(USERCMD, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            content += line
            if 'em_placeholder' in line:
                break
    for alias, v in alias_dict.items():
        param = f'{v["param"]}\n' if 'param' in v else ''
        content += f'\n[em_{alias}]\ncmd=cmd.exe /k {v["cmd"]}\n{param}'
    print(content)
    with open(USERCMD, 'w', encoding='utf-8') as f:
        f.write(content)

    # write wincmd
    content = after = ''
    # read user defined commands (not from alias)
    state = 'log_before'
    with open(WINCMD, 'r', encoding='utf-16') as f:
        for line in f.readlines():
            if state == 'log_before':  # log content before [Alias]
                content += line
            if '[Alias]' in line:  # ignore Alias (all alias from this py)
                state = 'log_alias'
                continue
            if state == 'log_alias' and line.startswith('['):  # log after part
                state = 'log_after'
            if state == 'log_after':
                after += line
    for alias, cmd in alias_dict.items():
        content += f'{alias}=em_{alias}\n'
    content += after
    with open(WINCMD, 'w', encoding='utf-16') as f:
        f.write(content)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    alias_to_totalcmd()
