#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# generate sidebar for docsify, list all markdown files.
# file/folder starts with '_' will be add to a PRIVATE file only.
# export '_sidebar.md' & '_sidebar_private.md', toggle by some private key.

import os
from urllib.parse import quote, unquote

# ═══════════════════════════════════════════════


def update_file(file, content):
    # read old file. If changes, update file.
    old = ''
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            old = f.read()

    # overwrite file if something new
    path, fn = os.path.split(file)
    if old.strip() != content.strip():
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {fn}')
    else:
        print(f'{fn} - has no change')


def add_content(fullpath, root):
    print(f'add content: {fullpath}')

    # calculate indent
    relative_path = fullpath.replace('\\', '/')[len(root):].lstrip('/')
    print(f'{relative_path = }')
    indent = relative_path.count('/') * '    '  # indent level
    levels = f'/{relative_path}'.split('/')  # per folder in path

    if not relative_path:
        return 'error', 'root'  # skip root

    # get file/folder name
    filename = levels[-1]
    # replace '_' with space in sidebar
    filename = filename[0] + filename[1:].replace('_', ' ')
    print(f'{filename = }')

    # skip sidebar file
    if filename.startswith('_sidebar') and fullpath.endswith('.md'):
        return 'error', 'sidebar.md'

    # generate line
    _type = 'public'  # if sidebar authority private

    if fullpath.endswith('.md'):
        # generate file entrance.
        filename = filename.lstrip("_")[:-3]  # remove '_' and '.md'
        line = f'{indent}- [**{filename}**]({quote(relative_path)})\n'
    else:  # folder
        line = f'{indent}- **{filename}**\n'

    # filter private path or file (starts with '_')
    for name in levels:
        if name.startswith('_'):
            _type = 'private'
            break

    print(f'{_type = } | {line}')
    return _type, line


def generate_sidebar(root=None, ignoreFolders=None):
    ignoreFolders = [] if ignoreFolders is None else ignoreFolders
    ignoreFolders += ['.git']
    if root is None:
        root = os.getcwd()  # the path of command line

    md = md_private = ''  # markdown file content

    for path, dirs, files in os.walk(root):  # read all files
        dirs[:] = [d for d in dirs if d not in ignoreFolders]

        if (path.endswith('.assets')):  # skip assets folder
            continue

        # add folder name to menu
        _type, line = add_content(path, root)
        if _type in ['public', 'private']:
            if _type == 'public':
                md += line
            md_private += line

        # add file to menu
        for fn in files:
            if fn.endswith('md'):
                print(f'===\n{fn = }')
                # generate sidebar
                _type, line = add_content(os.path.join(path, fn), root)
                if _type in ['public', 'private']:
                    if _type == 'public':
                        md += line
                    md_private += line

    # print(f'_sidebar.md\n{md}\n-----\n\n_sidebar_private.md\n{md_private}')

    update_file(os.path.join(root, '_sidebar.md'), md)
    update_file(os.path.join(root, '_sidebar_private.md'), md_private)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    DOCSIFY_ROOT = 'D:/OneDrive/site/notebook'
    for root, ignoreFolders in [
        [DOCSIFY_ROOT, ['shanghaitong']],  # docsify root
        # [DOCSIFY_ROOT + '/shanghaitong', []]  # 上海地方志
    ]:
        generate_sidebar(root, ignoreFolders)
