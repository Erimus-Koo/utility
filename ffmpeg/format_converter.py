#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 批量转文件格式
# 输出文件在命令运行目录

from erimus.toolbox import *
import subprocess
import pyperclip
import fire

# ═══════════════════════════════════════════════


def converter(fn=None, out_ext='mp3', bitrate=None):
    print(f'{sys.argv = }')
    if len(sys.argv) == 1:
        sys.argv.append(pyperclip.paste())
    print(f'Output format: {out_ext}')
    file_list = []
    for arg in sys.argv[1:]:
        print(f'{arg = }')
        arg = arg.strip('"')
        if os.path.isdir(arg):
            print(f'isdir')
            for path, dirs, files in os.walk(arg):  # read all files
                for fn in files:
                    print(f'{fn = }')
                    file_list.append(os.path.join(path, fn))
                break  # root only
        elif os.path.isfile(arg):
            print(f'isfile')
            file_list = [arg]
        else:
            print(f'Unknown: {arg = }')

    for fn in file_list:
        name, ext = os.path.splitext(fn)
        out = f'{name}.{out_ext}'
        if ext == f'.{out_ext}' or os.path.exists(out):
            continue

        if bitrate is None:
            try:
                res = subprocess.check_output(['ffmpeg', '-i', fn],
                                              stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                res = e.output       # Output generated before error
                code = e.returncode   # Return code
                print(f'{res = } {code = }')
            bitrate = re.search(r'Audio:.*?(\d+) kb/s', res.decode('utf-8'))
            bitrate = bitrate.group(1) if bitrate else ''
            print(f'{bitrate = }')
            if not bitrate.isdigit():  # if get bitrate, use origin. else, input.
                bitrate = input(f'Please input bitrate: 192 kb/s') or 192
            else:
                bitrate = min(int(bitrate), 192)  # max 192kb/s
            print(f'{bitrate = }')
        assert str(bitrate).isdigit()

        if out_ext == 'mp3':
            cmd = f'ffmpeg -i "{fn}" -map_metadata 0 -acodec libmp3lame -ab {bitrate}k "{out}"'
        elif out_ext == 'ao':
            cmd = f'ffmpeg -i "{fn}" -c:a copy "{name}_audio_only.mp4"'
        elif out_ext == 'mp4':
            cmd = f'ffmpeg -i "{fn}" -c copy "{out}"'
        else:  # 还没搞清楚具体格式用法
            cmd = f'ffmpeg -i "{fn}" -c copy "{out}"'

        print(cmd)
        os.system(cmd)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # converter()
    fire.Fire(converter)
