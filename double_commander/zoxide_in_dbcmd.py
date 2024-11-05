#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
1. 传入当前面板的路径和左右面板的路径，判断当前激活的是哪侧面板。
2. 调用 zoxide，获得返回的路径。
3. 让 dbcmd 在当前面板开启路径。

parameters in double command:
/Users/erimus/OneDrive/05ProgramProject/Python/utilities/share/double_commander/zoxide_in_dbcmd.py --query "%[Zoxide: Jump to folder. (starts with "zz " to list & choice);]" --current_path %D --left_panel_path %Dl
'''

import logging as log
import os
import re
import subprocess
import time
import tkinter as tk
from tkinter import Listbox, Scrollbar

import fire

# ==================================================
fn, _ = os.path.splitext(os.path.basename(__file__))
LOG_FILE = os.path.expanduser(f'~/log/{fn}.log')

# 配置 logging 模块
fh = log.FileHandler(LOG_FILE, encoding='utf-8')
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers=[fh, log.StreamHandler()])
# ==================================================
TARGET_PATH = ''
zoxide = '/opt/homebrew/bin/zoxide'
# ==================================================


def get_zoxide_paths(query: str) -> list[str]:
    '''
    Searches for paths in zoxide.

    Args:
        query (str): The search query.

    Returns:
        list[str]: A list of strings in the format '{score} | {path}'.
    '''
    query_list = [q for q in query.split(' ') if q]
    try:
        # 使用 subprocess 获取 zoxide 查询结果
        cmd = [zoxide, 'query', '-s', '-l'] + query_list
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                check=True)
        path_list = []
        for l in result.stdout.strip().split('\n'):
            match = re.search(r'^(\d+) (.*)$', l.strip())
            score, path = match.groups()
            path_list.append(f'{score:>5s} | {path}')
        return path_list
    except subprocess.CalledProcessError:
        log.error("Error: Could not find the specified directories in zoxide.")
        return []


def show_path_selector(path_list: list[str]) -> None:
    '''
    Opens a GUI path selector.

    Args:
        path_list (list[str]): A list of paths to display in the selector.

    Modifies:
        TARGET_PATH (str): A global variable that holds the selected path.
                           The modification occurs because the GUI cannot return a variable before destruction,
                           and it cannot return a variable after destruction.
    '''
    root = tk.Tk()
    root.title("Select Directory")

    # 确保窗口总在最上层
    root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)

    font = ('JetBrainsMono Nerd Font', 16)
    listbox = Listbox(root, selectmode=tk.SINGLE, font=font)
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # 给列表插入地址
    for path in path_list:
        listbox.insert(tk.END, path)

    # 默认选中第一条
    listbox.selection_set(0)

    def on_up(event):
        current_selection = listbox.curselection()
        print(f'---\n{current_selection = }')
        if current_selection:
            index = current_selection[0]
            print(f'{index = }')
            if index > 0:
                listbox.selection_clear(index)
                listbox.selection_set(index - 1)

    def on_down(event):
        current_selection = listbox.curselection()
        print(f'---\n{current_selection = }')
        if current_selection:
            index = current_selection[0]
            print(f'{index = }')
            if index < listbox.size() - 1:
                listbox.selection_clear(index)
                listbox.selection_set(index + 1)

    def on_ok():
        global TARGET_PATH
        selected_index = listbox.curselection()
        if selected_index:
            TARGET_PATH = listbox.get(selected_index[0])
        else:
            TARGET_PATH = listbox.get(0)  # 默认选中第一条
        log.info(f'✅ Selected {TARGET_PATH = }')
        root.destroy()

    def on_cancel():
        global TARGET_PATH
        TARGET_PATH = None
        log.info("Cancel Select")
        root.destroy()

    # 绑定上下键
    listbox.bind('<Up>', on_up)
    listbox.bind('<Down>', on_down)

    # 绑定回车键
    root.bind('<Return>', lambda event: on_ok())

    # 绑定双击事件
    listbox.bind('<Double-1>', lambda event: on_ok())

    # 确认按钮
    # ok_button = tk.Button(root, text="OK", command=lambda: on_ok())
    # ok_button.pack(pady=10)

    # 绑定Esc键
    root.bind('<Escape>', lambda event: on_cancel())

    # 确保 Tkinter 窗口聚焦到列表
    root.after(100, lambda: listbox.focus_force())

    root.mainloop()


def open_double_commander(panel: list['l', 'r'], path: str) -> None:
    '''
    Opens a specified path in the Double Commander panel.

    Args:
        panel (list['l', 'r']): The target panel in Double Commander.
        path (str): The file system path to open in the specified panel.
    '''
    try:
        # 使用 open 命令启动 Double Commander 并传递路径参数
        cmd = [
            'open', '-n', '-a', 'Double Commander', '--args', f'-{panel}', path
        ]
        log.info(f'🎹 {cmd = }')
        subprocess.run(cmd)
    except Exception as e:
        log.error(f"Error: {e}")


def main(
        query: str,  # query from user input in dbcmd
        current_path: str,  # path of current panel
        left_panel_path: str,  # path of left panel
        *args,
        **kwargs) -> None:
    global TARGET_PATH
    log.info(f'{query = }')
    log.info(f'{current_path = }')
    log.info(f'{left_panel_path = }')
    # log.info(f'{args = }')
    # log.info(f'{kwargs = }')

    # if directly search query, or return a path list for select
    select_mode = False
    for arg_list in ['l', 'zz', 'zi']:
        if query.startswith(f'{arg_list} '):
            query = query.removeprefix(f'{arg_list} ')
            select_mode = True
            break

    # which panel is active
    panel = 'l' if current_path == left_panel_path else 'r'
    log.info(f'{panel = }')

    # 如果传入的是完整路径
    if os.path.exists(query):
        if os.path.isfile(query):  # 如果是文件 取其目录
            query = os.path.dirname(query)

        print(f'Full path {query = }')
        subprocess.run((zoxide, 'add', query))  # add path to zoxide
        open_double_commander(panel, query)  # open path
        return

    # if query is keyword, search in zoxide
    path_list = get_zoxide_paths(query)
    print(f'{path_list = }')
    if not path_list:
        log.info('❌ Found nothing.')
        return

    # if open the path select window
    if select_mode and len(path_list) > 1:
        show_path_selector(path_list)
    else:
        TARGET_PATH = path_list[0]

    TARGET_PATH = TARGET_PATH.split(' | ', 1)[-1]

    log.info(f'{TARGET_PATH = }')
    if os.path.exists(TARGET_PATH):
        open_double_commander(panel, TARGET_PATH)
    else:
        log.error(f'❌ Path does not exist')


# ==================================================

if __name__ == '__main__':

    # query = 'logo'
    # left_panel_path = '~/'
    # current_path = '~/Downloads'  # current is right
    # main(query, current_path, left_panel_path)
    fire.Fire(main)
