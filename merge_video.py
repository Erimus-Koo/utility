#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# merge audio/video/sub what download from youtube
# e.g. a[00].mp4 | a[01].mp4 | a.en.srt

import os
import fire

# ═══════════════════════════════════════════════


def merge_video(root=None):
    root = os.getcwd() if root is None else root

    video_dict = {}
    # find video file
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            name, ext = os.path.splitext(fn)
            if ext in ['.mp4', '.webm', '.flv']:
                if name.endswith('[00]'):
                    video_dict[name[:-4]] = {'video': '', 'audio': '',
                                             'sub': [], 'ext': ext}

        break  # root only

    # find all assets of video
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            for video_name, info in video_dict.items():
                if fn.startswith(video_name):
                    name, ext = os.path.splitext(fn)
                    if name[-4:] == '[00]':
                        info['video'] = fn
                    elif name[-4:] == '[01]':
                        info['audio'] = fn
                    elif ext == '.srt':
                        info['sub'].append(fn)

        break  # root only

    print(video_dict.keys())

    # merge video
    for video_name, info in video_dict.items():
        if not (info['video'] and info['audio']):  # 必须音视频齐全
            continue
        assets = [info['video'], info['audio']] + info['sub']
        out = video_name + info['ext']
        info_cmd = ''.join([f' -i "{f}"' for f in assets])

    cmd = f'ffmpeg{info_cmd} -c copy "{out}"'
    print(f'>>> {cmd}')
    os.system(cmd)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(merge_video)
