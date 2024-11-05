#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from webdriver_manager.core.utils import get_browser_version_from_os
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import re
import sys
import shutil

# ═══════════════════════════════════════════════
ver_dict = {
    # windowsx 下载一种驱动
    'win32': [['win32', 'D:/OneDrive/Misc/path']],
    # mac 下载两种
    'darwin': [
        ['mac64', '/Users/erimus/OneDrive/Misc/path'],
        ['mac_arm64', '/Users/erimus/path'],
    ],
}
# ═══════════════════════════════════════════════


def update_chrome_driver(name, drv_path):
    # 获取当前系统chrome浏览器的版本号
    browser_ver = get_browser_version_from_os("google-chrome")
    print(f'{browser_ver = }')
    main_ver = browser_ver.split(".")[0]  # 获取浏览器的主版本号
    print(f'{main_ver = }')

    res = requests.get(url="https://chromedriver.storage.googleapis.com")
    content = res.text
    ver_list = re.search(
        f'({main_ver}.\\d+.\\d+.\\d+)/chromedriver_{name}.zip', content, re.S)
    if ver_list is None:
        print(f'Not found ver [{main_ver}]')
        return
    else:
        available_ver = ver_list.group(1)

    print(f'{available_ver = }')
    # 这里可以加参数path 其实是在path下再创建`.wdm`目录 所以没有意义
    install_path = ChromeDriverManager(version=available_ver).install()
    print(f'{install_path = }')

    _, fn = os.path.split(install_path)
    dst_path = os.path.join(drv_path, fn)
    shutil.copy(install_path, dst_path)
    print(f'src: {install_path}\ndst: {dst_path}')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    # for name, drv_path in ver_dict[sys.platform]:
    #     update_chrome_driver(name, drv_path)

    install_path = ChromeDriverManager().install()
    print(f'{install_path = }')

    _, fn = os.path.split(install_path)
    dst_path = os.path.join('/Users/erimus/path', fn)
    shutil.copy(install_path, dst_path)
    print(f'src: {install_path}\ndst: {dst_path}')
