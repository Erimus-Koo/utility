#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# generate sidebar for docsify, list all markdown files.
# file/folder starts with '_' will be add to a PRIVATE file only.
# export '_sidebar.md' & '_sidebar_private.md', toggle by some private key.

import os

# ═══════════════════════════════════════════════
md = md_private = ''
# ═══════════════════════════════════════════════


def add_content(fullpath):
    global md, md_private
    fullpath = fullpath.replace('\\', '/')
    fullpath = fullpath[len(root):].lstrip('/')
    if not fullpath:
        return  # skip root
    indent = fullpath.count('/') * '    '  # indent level
    levels = f'/{fullpath}'.split('/')  # per folder in path
    filename = levels[-1]  # get file/folder name
    # ignore sidebar file
    if filename.startswith('_sidebar') or '.assets' in fullpath:
        return
    filename = filename[0] + filename[1:].replace('_', ' ')

    # generate line
    if fullpath.endswith('.md'):
        line = f'{indent}- [**{filename[:-3]}**]({fullpath})'
    else:  # folder
        line = f'{indent}- **{filename}**'

    # add line to public md
    for name in levels:
        if name.startswith('_'):
            break
    else:  # all path(self or parent) is not private
        md += f'{line}\n'

    # add line to private
    line = line.replace('**_', '**')  # remove private underscore in display
    md_private += f'{line}\n'


def update_file(file, content):
    with open(file, 'r', encoding='utf-8') as f:
        old = f.read()
    fn = file.split('\\')[-1]
    if old.strip() != content.strip():
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {fn}')
    else:
        print(f'{fn} - has no change')


def generate_sidebar(root=None, ignoreFolders=None):
    global md, md_private
    ignoreFolders = [] if ignoreFolders is None else ignoreFolders
    if root is None:
        root = os.getcwd()  # the path of command line

    md = md_private = ''

    for path, dirs, files in os.walk(root):  # read all files
        dirs[:] = [d for d in dirs if d not in ignoreFolders]
        path_wrote = False
        for fn in files:
            if fn.endswith('md'):
                # if folder is empty, it need not to be write.
                if not path_wrote and not fn.startswith('_'):
                    add_content(path)
                    path_wrote = True
                # add md file
                add_content(os.path.join(path, fn))

    # print(f'_sidebar.md\n{md}\n-----\n\n_sidebar_private.md\n{md_private}')

    update_file(os.path.join(root, '_sidebar.md'), md)
    update_file(os.path.join(root, '_sidebar_private.md'), md_private)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    root = r'D:\OneDrive\site\notebook'  # my docsify root
    ignoreFolders = ['.git', '上海通']
    generate_sidebar(root, ignoreFolders)
