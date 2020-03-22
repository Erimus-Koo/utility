#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
整理一些常用目录的文件，替代手工重复操作。
备份目录中的文件命名规则：在第一个下划线前为软件名称，长名称需连写。
e.g. totalcommand_202003220231.json
'''

from datetime import datetime
import os
import re

# ═══════════════════════════════════════════════
DOWNLOAD = 'D:/Downloads'  # chrome默认下载目录
BT_DOWNLOAD = 'D:/Downloads/av'  # 影视下载目录
SETTING_BACKUP = 'D:/OneDrive/Misc/setting_backup'  # 设置文件备份目录
APPDATA = os.getenv('APPDATA')
TIME = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')  # 当前时间
# ═══════════════════════════════════════════════
delete_files = []  # 需要删除的文件
copy_files = []  # 需要备份的文件
backup_dict = {}  # 已备份的最新文件
# ═══════════════════════════════════════════════


def read_backup_file():
    result = {}
    for path, dirs, files in os.walk(SETTING_BACKUP):  # read all files
        for fn in files:
            file = os.path.join(path, fn)  # full path
            app_name = fn.split('_')[0]
            result.setdefault(app_name, [])
            result[app_name].append(file)
    for app_name, files in result.copy().items():
        result[app_name] = max(files)  # 以文件名最大的文件为最新文件
    return result


def different(file1, file2):
    if not file1 or not file2:
        return True
    with open(file1, 'rb') as f:
        data1 = f.read()
    with open(file2, 'rb') as f:
        data2 = f.read()
    if data1 != data2:
        return True


def backup_setting_file(source, app_name):
    global backup_dict
    if different(source, backup_dict.get(app_name)):
        print(f'{app_name.title()} setting updated.')
        fn, ext = os.path.splitext(source)
        target = os.path.join(SETTING_BACKUP, f'{app_name}_{TIME}{ext}')
        copy_files.append((source, target))


def main():
    global backup_dict
    backup_dict = read_backup_file()

    # 删除torrent文件
    for root, dirname, files in os.walk(BT_DOWNLOAD):
        for fn in files:
            if fn.endswith('.torrent'):
                delete_files.append(os.path.join(root, fn))
        break

    # typora 主题
    typora = os.path.join(APPDATA, 'Typora/themes/typora_erimus.css')
    backup_setting_file(typora, 'typora')

    # listary 设置
    listary = os.path.join(APPDATA, 'Listary/UserData/Preferences.json')
    backup_setting_file(listary, 'listary')

    # mactype
    mactype = 'C:/Program Files/MacType/ini/Erimus.ini'
    backup_setting_file(mactype, 'mactype')

    # totalcmd 配置
    totalcmd = 'D:/Program Files/TotalCMD64/Wincmd.ini'
    backup_setting_file(totalcmd, 'totalcmd')

    # setpoint 配置
    setpoint = os.path.join(APPDATA, 'Logitech/SetPoint/user.xml')
    backup_setting_file(setpoint, 'setpoint')

    # mskeyboard
    mskeyboard = 'D:/system/Documents/Microsoft Hardware/Macros/end.mhm'
    backup_setting_file(mskeyboard, 'mskeyboard')

    # download folder
    for path, dirs, files in os.walk(DOWNLOAD):  # read all files
        for fn in files:
            fn = fn.lower()
            file = os.path.join(path, fn)  # full path
            # 移动各软件的配置文件备份
            for bk_file in ['OmegaOptions.bak',
                            'potplayer.reg',
                            'saladict.saladict',
                            'stylus.json',
                            'tampermonkey.txt',
                            'ublock.txt']:
                app, ext = bk_file.lower().split('.')
                if app in fn and fn.endswith(ext):
                    app_backup = os.path.join(path, fn)
                    backup_setting_file(app_backup, app)
                    delete_files.append(file)

            # 删除下载的软件升级安装包
            for name in ['FalconX', 'PowerToysSetup']:
                if name.lower() in fn:
                    delete_files.append(file)

            # 删除字幕文件
            if re.findall(r'\d{15}\.(zip|rar)', fn.lower()):
                print(f'Found Subtitle: {fn}')
                delete_files.append(file)

        break  # root only

    # 复制备份文件
    for source, target in copy_files:
        source = source.replace('/', '\\')
        target = target.replace('/', '\\')
        print(source)
        print(target)
        os.system(f'copy "{source}" "{target}"')

    # 删除文件
    for file in delete_files:
        print(f'Delete file: {file}')
        os.remove(file)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    main()
