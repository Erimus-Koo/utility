#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 传入 project_folder (git_root) 等参数，寻找该 git 目录的 pack 中的大文件。
# 结果保存在 project_folder 下的 git_pack_big_files.xlsx

import os
import subprocess
from io import StringIO
import pandas as pd
import re
import fire

# ═══════════════════════════════════════════════


def title(text):
    print(f'\n{text.capitalize()} '.ljust(50, '='))


def find_git_pack_big_file(
    project_folder=None,        # 项目所在目录 默认用cwd
    count=100,                  # 显示前N个
    size=100000,                # 显示大于100k的文件
):
    if project_folder is None:
        project_folder = os.getcwd()

    # find idx file
    pack_folder = os.path.join(project_folder, '.git/objects/pack')
    idx_files = [f for f in os.listdir(pack_folder) if f.endswith('.idx')]
    print(f'{idx_files = }')
    if not idx_files:
        print(f'Can not find pack file at: {pack_folder}')

    title('get file size')
    verify_headers = ['SHA-1', 'type', 'size', 'size-in-packfile',
                      'offset-in-packfile', 'depth', 'base-SHA-1']
    pack_df = pd.DataFrame(columns=verify_headers)
    for idx_file in idx_files:
        idx_file = os.path.join(pack_folder, idx_file)
        cmd = f'git verify-pack -v "{idx_file}"'
        print(f'{cmd = }')
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.decode('utf-8')
        out = out[:out.index('non delta:')].strip()
        this_df = pd.read_csv(StringIO(out), delim_whitespace=True,
                              names=verify_headers)
        pack_df = pd.concat([pack_df, this_df], axis=0)
        pack_df.set_index('SHA-1', inplace=True)
    print(f'{pack_df = }')

    title('calculate average size')
    pack_df['avg'] = pack_df[['size', 'size-in-packfile']].mean(axis=1)\
        .astype(int)
    pack_df = pack_df[pack_df['avg'] > size]
    pack_df.sort_values('avg', ascending=False, inplace=True)
    pack_df = pack_df[:count]
    print(f'{pack_df = }')

    title('get file name')
    cmd = f'git --git-dir="{project_folder}/.git" rev-list --objects --all'
    print(f'{cmd = }')
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.stdout.decode('utf-8')
    reg_valid_data = re.compile(r'[0-9a-z]{40}\s.+')
    r = []
    for line in out.split('\n'):
        if reg_valid_data.match(line):
            # print(line)
            r.append([line[:40], line[41:]])
    fn_df = pd.DataFrame(r, columns=['SHA-1', 'filename'])
    fn_df.set_index('SHA-1', inplace=True)
    print(f'{fn_df = }')

    title('merge data')
    pack_df = pd.concat([pack_df, fn_df], axis=1, join='inner')
    print(f'{pack_df = }')

    df = pack_df.rename_axis('SHA-1').reset_index()
    df = df[['size', 'size-in-packfile', 'avg', 'filename']]
    # print setting
    df.reset_index(drop=True, inplace=True)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(f'{df}')

    title('output')
    output = os.path.join(project_folder, 'git_pack_big_files.xlsx')
    df.to_excel(output)
    print(f'{output = }')


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    fire.Fire(find_git_pack_big_file)
