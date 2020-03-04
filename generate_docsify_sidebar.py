#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# generate sidebar for docsify, list all markdown files.
# file/folder starts with '_' will be add to a PRIVATE file only.
# export '_sidebar.md' & '_sidebar_private.md', toggle by some private key.

import os

# ═══════════════════════════════════════════════


def generate_sidebar(root=None):
    if root is None:
        root = os.getcwd()  # the path of command line

    md = []  # result md
    md_private = []

    def add_content(fullpath):
        fullpath = fullpath.replace('\\', '/')
        fullpath = fullpath[len(root):].lstrip('/')
        if not fullpath:
            return  # skip root
        indent = fullpath.count('/') * '    '  # indent level
        levels = f'/{fullpath}'.split('/')
        filename = levels[-1]  # get file/folder name
        if filename.startswith('_sidebar'):  # ignore sidebar file
            return

        # generate line
        if fullpath.endswith('.md'):
            line = f'{indent}- [**{filename[:-3]}**]({fullpath})'
        else:  # folder
            line = f'{indent}- **{filename}**'

        # add line to md
        for name in levels:
            if name.startswith('_') or name.endswith('.assets'):
                break
        else:  # all path(self or parent) is not private
            md.append(line)
        md_private.append(line)

    for path, dirs, files in os.walk(root):  # read all files
        path_wrote = False
        for fn in files:
            if fn.endswith('md'):
                # if folder is empty, it need not to be write.
                if not path_wrote:
                    add_content(path)
                    path_wrote = True
                # add md file
                add_content(os.path.join(path, fn))

    print('_sidebar.md\n')
    [print(i) for i in md]
    print('\n-----\n\n_sidebar_private.md\n')
    [print(i) for i in md_private]

    with open(os.path.join(root, '_sidebar.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    with open(os.path.join(root, '_sidebar_private.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_private))


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    root = 'D:/OneDrive/erimus-koo.github.io/notebook'  # my docsify root
    generate_sidebar(root)
