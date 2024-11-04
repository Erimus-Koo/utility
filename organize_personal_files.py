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
DOWNLOAD = 'G:/Downloads'  # chrome默认下载目录
BT_DOWNLOAD = 'G:/Downloads/av'  # 影视下载目录
BACKUP_FOLDER = 'D:/OneDrive/Misc/setting_backup'  # 设置文件备份目录
APPDATA = os.getenv('APPDATA')
TIME = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')  # 当前时间
# ═══════════════════════════════════════════════
delete_files = []  # 需要删除的文件
copy_files = []  # 需要备份的文件
BACKUP_DICT = {}  # 已备份的最新文件
# ═══════════════════════════════════════════════
# 从各软件所在目录读取设置并备份
SETTINGS_IN_SEPARATE = {
    'cmder': 'D:/Program Files/cmder/config/user-ConEmu.xml',
    'listary': os.path.join(APPDATA, 'Listary/UserData/Preferences.json'),
    'mactype': 'C:/Program Files/MacType/ini/Default.ini',
    'mskeyboard': 'D:/system/Documents/Microsoft Hardware/Macros/end.mhm',
    # 'musicbee': os.path.join(APPDATA, 'MusicBee/MusicBee3Settings.ini'),
    'musicbee': 'D:/Program Files/MusicBee/AppData/MusicBee3Settings.ini',
    'powershell':
    'D:/system/documents/PowerShell/Microsoft.PowerShell_profile.ps1',
    'setpoint': os.path.join(APPDATA, 'Logitech/SetPoint/user.xml'),
    # 'snipaste': 'D:/Program Files/Snipaste/config.ini',
    'totalcmd': 'D:/Program Files/TotalCMD64/Wincmd.ini',
    'totalcmd-usercmd': 'D:/Program Files/TotalCMD64/usercmd.ini',
    # 'typora': os.path.join(APPDATA, 'Typora/themes/typora-erimus.css'),
    'xnview': os.path.join(APPDATA, 'XnViewMP/xnview.ini'),
    'xnview-bookmark': os.path.join(APPDATA, 'XnViewMP/bookmark.ini'),
}

# 从下载目录读取下载的配置文件。
# 下载的备份文件经常有类似 stylus-2021-02-11.json 的形式
# 需要识别关键字 stylus 和后缀名 json
SETTINGS_IN_DOWNLOAD = [
    'OmegaOptions.bak',
    'PotPlayer.reg',
    'saladict.saladict',
    'stylus.json',
    'tampermonkey.txt',
    'ublock.txt',
    'auto-tab-discard.json',
    'vimium.json',
]
# ═══════════════════════════════════════════════
re_time = re.compile(r'_\d{4}(-\d\d){5}')


# 返回各个app最新版备份的文件名列表
def read_backup_file():
    result = {}  # {app name: most recent file}
    for path, dirs, files in os.walk(BACKUP_FOLDER):  # read all files
        for fn in files:
            file = os.path.join(path, fn)  # full path
            update_time = re_time.search(fn)
            if update_time:
                update_time = update_time.group(0)
                app_name = fn.split(update_time)[0]
                result.setdefault(app_name, [])
                result[app_name].append(file)
    for app_name, files in result.copy().items():
        result[app_name] = max(files)  # 以文件名最大的文件为最新文件
    # [print(k, v) for k, v in result.items()]
    return result


BACKUP_DICT = read_backup_file()  # {app name: most recent file}


# 比较文件内容是否有改动
def different(file1, file2):
    if not file1 or not file2:
        return True
    with open(file1, 'rb') as f:
        data1 = f.read()
    with open(file2, 'rb') as f:
        data2 = f.read()
    if data1 != data2:
        return True


# 备份设置文件
def backup_setting_file(setting_path, app_name):
    if not os.path.exists(setting_path):
        print(f'Not exists: {setting_path}')

    app_backup_folder = os.path.join(BACKUP_FOLDER, app_name)
    if not os.path.exists(app_backup_folder):
        os.mkdir(app_backup_folder)
    if different(setting_path, BACKUP_DICT.get(app_name)):  # 文件有改动时才更新
        print(f'{app_name.title()} setting updated.')
        fn, ext = os.path.splitext(setting_path)
        target = os.path.join(app_backup_folder, f'{app_name}_{TIME}{ext}')
        copy_files.append((setting_path, target))


def clean():

    # 删除torrent文件及下载相关
    for root, dirname, files in os.walk(BT_DOWNLOAD):
        for fn in files:
            if fn.endswith('.torrent'):
                delete_files.append(os.path.join(root, fn))
            if fn.endswith('.mp41'):  # zhuzhu zimu
                os.rename(os.path.join(root, fn), os.path.join(root, fn[:-1]))
        break

    # 备份各软件目录下的设置文件
    # for sname, spath in SETTINGS_IN_SEPARATE.items():
    #     backup_setting_file(spath, sname)

    # download folder
    for path, dirs, files in os.walk(DOWNLOAD):  # read all files
        for fn in files:
            fn = fn.lower()
            file = os.path.join(path, fn)  # full path
            # 移动各软件的配置文件备份 appname.ext(specific)
            for bk_file in SETTINGS_IN_DOWNLOAD:
                app_name, ext = bk_file.split('.')
                if app_name.lower() in fn and fn.endswith(ext.lower()):
                    backup_setting_file(file, app_name)
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

    print('Clean finished.')


def restore_settings():
    for app_name, target in SETTINGS_IN_SEPARATE.items():
        source = BACKUP_DICT.get(app_name)
        if source:
            if not os.path.exists(target):  # 无配置文件
                print(f'\n"{target}" not exists.')
                # os.system(f'copy "{source}" "{target}"')

            elif different(source, target):  # 配置文件与备份不同
                print(f'\n"{source}" different from \n"{target}"')
                # os.system(f'copy "{source}" "{target}"')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    clean()

    # restore_settings()
