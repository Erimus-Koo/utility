#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from webdriver_manager.core.utils import get_browser_version_from_os
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import re
import shutil

# ═══════════════════════════════════════════════
ver_dict = {
    'win32': '/Users/erimus/OneDrive/Misc/path',
    'mac64': '/Users/erimus/OneDrive/Misc/path',
    'mac64_m1': '/Users/erimus/path',
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
        f'({main_ver}.\\d+.\\d+.\\d+)/chromedriver_{name}.zip',
        content, re.S)
    if ver_list is None:
        print(f'Not found ver [{main_ver}]')
        return
    else:
        available_ver = ver_list.group(1)

    print(f'{available_ver = }')
    # 这里的path参数好像没用 所以自己复制一份到目标位置
    install_path = ChromeDriverManager(version=available_ver,
                                       path=drv_path).install()
    print(f'{install_path = }')

    folders = install_path.split(os.path.sep)
    for name, path in ver_dict.items():
        if name in folders:
            _, fn = os.path.split(install_path)
            dst_path = os.path.join(path, fn)
            shutil.copy(install_path, dst_path)
            print(f'src: {install_path}\ndst: {dst_path}')
            break


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    update_chrome_driver('mac64_m1', '/Users/erimus/path')
