#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
1. Add modify time as suffix to the file name
2. Check if the file has same name in the archive folder
3. If not, move current file to the archive folder with new name
'''

import logging as log
import os
import re
import shutil
import time

import fire

# ==================================================
fn, _ = os.path.splitext(os.path.basename(__file__))
LOG_FILE = os.path.expanduser(f'~/log/{fn}.log')

# 配置 logging 模块
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers=[
                    log.FileHandler(LOG_FILE, encoding='utf-8'),
                    log.StreamHandler()
                ])


def check_archive_folder(file):
    """Check if the archive folder exists, if not, create it."""
    path, _ = os.path.split(file)
    archive_folder = os.path.join(path, 'backup__archive')
    if not os.path.exists(archive_folder):
        os.mkdir(archive_folder)
        log.info(f"Created archive folder: {archive_folder}")
    return archive_folder


def get_archive_file_name(file):
    """Generate the archived file name with modification time."""
    try:
        mtime = os.path.getmtime(file)
        formatted_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(mtime))
        base_name, ext = os.path.splitext(os.path.basename(file))
        new_base_name = re.sub(r'_\d{8}-\d{6}$', '', base_name)
        new_base_name = re.sub(r'_\d{8}$', '', new_base_name)
        new_fn = f"{new_base_name}_{formatted_time}{ext}"
        return new_fn
    except Exception as e:
        log.info(f"Error getting archive file name for {file}: {e}")
        return None


def main(*files):
    """Main function to archive files."""
    log.info(f"Script started with files: {files}")

    for file in files:
        try:
            archive_folder = check_archive_folder(file)
            new_fn = get_archive_file_name(file)
            if new_fn is None:
                continue
            archive_file = os.path.join(archive_folder, new_fn)
            if not os.path.exists(archive_file):
                shutil.copy(file, archive_file)
                log.info(f"Copied {file} to {archive_file}")
            else:
                log.info(f"File {archive_file} already exists")
        except Exception as e:
            log.info(f"Error processing file {file}: {e}")

    log.info("Script finished")


# ==================================================

if __name__ == '__main__':

    file = '/Users/erimus/OneDrive/21MoSeeker/50运营/MoTalk_AfterMoTea/MoTalk13/Invitation/qr-code.svg'
    # main(file)

    fire.Fire(main)
