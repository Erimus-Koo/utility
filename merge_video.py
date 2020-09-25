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

    out = None
    video_dict = {}
    # find video file
    for path, dirs, files in os.walk(video_root):  # read all files
        for fn in files:
            name, ext = os.path.splitext(fn)
            if out is None:
                out = os.path.join(path, name + '_merge' + ext)
            if ext in ('.mp4', '.webm', '.flv', '.ts'):
                video_dict.setdefault(ext, [])
                if root is None:
                    video_dict[ext].append(fn)
                else:
                    video_dict[ext].append(os.path.join(video_root, fn))
        break  # root only

    # merge video
    for ext, video_list in video_dict.items():
        print(f'Merge [{ext}] videos'.ljust(50, '='))
        [print(i) for i in video_list]
        input('Merge all above videos, press enter to continue...')
        if ext == '.ts':
            src = '+'.join([f'"{v}"' for v in video_list])
            cmd = f'copy /b {src} "{out}"'
        else:
            info_cmd = ''.join([f' -i "{f}"' for f in video_dict])
            cmd = f'ffmpeg{info_cmd} -c copy "{out}"'
        print(f'{"+"*50}\n{cmd}\n{"+"*50}')
        os.system(cmd)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    fire.Fire(merge_video)
