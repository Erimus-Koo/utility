#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# merge audio/video/sub what download from youtube
# e.g. a[00].mp4 | a[01].mp4 | a.en.srt

import os
import fire

# ═══════════════════════════════════════════════


def merge_video(root=None):
    video_root = os.getcwd() if root is None else root
    print(f'{video_root = }')

    out_file = None
    temp_file_list = ''
    # find video file
    for path, dirs, files in os.walk(video_root):  # read all files
        for fn in files:
            name, ext = os.path.splitext(fn)
            if ext not in ('.mp4', '.webm', '.flv', '.ts'):
                continue
            if out_file is None:
                out_file = os.path.join(path, name + '_merge' + ext)
            file = os.path.join(path, fn)
            temp_file_list += f"file '{file}'\n"
        break  # root only

    if not temp_file_list:
        print(f'No video files in "{video_root}"')
        return

    # merge video
    video_list_txt = os.path.join(video_root, f'file_list.txt')
    with open(video_list_txt, 'w', encoding='utf-8') as f:
        f.write(temp_file_list)
    cmd = f'ffmpeg -f concat -safe 0 -i {video_list_txt} -c copy "{out_file}"'
    os.system(cmd)

    # check output
    if os.path.exists(out_file):
        print(f'Merge success: "{out_file}"')
    else:
        print(f'Merge failed !!!')


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(merge_video)
