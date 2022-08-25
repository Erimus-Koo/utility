#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# Run a service to receive keys, and "replay" keys on local.
# Use rest api, for example:
# http://10.0.0.13:8836/send?key=ctrl_a

import os
import sys
import cgi
from wsgiref.simple_server import make_server
import pyautogui
import subprocess
import psutil
import time
from util.kill_process import kill_process
from util.windows_keep_awake import keep_awake_on, keep_awake_off
from util.gym_timer import gym_plus_one
from erimus.homeassistant_restapi import turn, state

# ═══════════════════════════════════════════════
pyautogui.FAILSAFE = False  # screen off keep working
software_dict = {
    'musicbee': r'D:\Program Files\MusicBee\MusicBee.exe',
    'cloudmusic': r'C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe',
    'spotify': r'C:\Users\chuan\AppData\Roaming\Spotify\Spotify.exe',
}
musicplayer = 'cloudmusic'
# ═══════════════════════════════════════════════


class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function


# ═══════════════════════════════════════════════


def process_exists(pname):
    for p in psutil.process_iter():
        try:  # sometime do not has name
            if pname.lower() in p.name().lower():
                return True
        except Exception:
            pass


# 立刻锁屏
def screen_off():
    keep_awake_off()
    for _process in ['potplayer', 'cloudmusic', 'spotify', 'musicbee',
                     'firefox']:
        kill_process(_process)
    # os.popen('nircmd monitor off')  # 息屏


# ═══════════════════════════════════════════════


def rest_api(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']
    msg = f'[{os.getpid()}] '

    # 快捷键部分
    if 'key' in params:
        key = params['key'].lower()
        # play key on local
        if '_' in key:
            keys = key.split('_')
            msg += f'HOTKEY: {keys}'
            pyautogui.hotkey(*keys)
        else:
            msg += f'PRESS: {key}'
            pyautogui.press(key)
        params.pop('key')

    # 开启软件部分
    if 'open' in params:
        software = params['open'].lower()
        if software == 'musicplayer':
            software = musicplayer
        if software in software_dict:
            if process_exists(software):
                msg += f'[{software}] is already running.'
            else:
                msg += f'Launch: {software_dict[software]}'
                os.startfile(software_dict[software])
        else:
            software_list = '\n'.join(software_dict)
            msg += (f'<pre>\nNot support this software: {software}\n'
                    f'Supported List:\n{software_list}\n</pre>')
        params.pop('open')

    # 运行命令
    if 'run' in params:
        cmd = params['run'].lower()
        args = []
        if '(' and ')' in cmd:
            cmd, args = cmd.split('(')
            args = [p.strip() for p in args.replace(')', '').split(',')]
        print(f'{cmd = } | {args = }')
        try:
            r = eval(cmd)(*args)
            if r:
                msg = r
            else:
                msg += f'Run [{cmd}] success.'
        except Exception:
            msg += f'Run [{cmd}] failed.'
        params.pop('run')

    # 语音
    if 'say' in params:
        say_content = params['say']
        msg += f'Say: {say_content}'
        os.system(f'nircmd speak text "{say_content}"')
        params.pop('say')

    if params:  # 还有其它参数
        msg += f'Not Defined Params: {environ["params"]}'

    print(msg)
    yield f'{msg}\n'.encode('utf-8')


# ═══════════════════════════════════════════════


def notfound_404(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    info = '''
<pre>

# Remote Key

Use "pyautogui" play keys, only accept "press" & "hotkey"
Shortcuts concat by "_", like "ctrl_a".

Mediakey:
    'volumemute': 0xad, # VK_VOLUME_MUTE
    'volumedown': 0xae, # VK_VOLUME_DOWN
    'volumeup':   0xaf, # VK_VOLUME_UP
    'nexttrack':  0xb0, # VK_MEDIA_NEXT_TRACK
    'prevtrack':  0xb1, # VK_MEDIA_PREV_TRACK
    'stop':       0xb2, # VK_MEDIA_STOP
    'playpause':  0xb3, # VK_MEDIA_PLAY_PAUSE

Read more:
    https://pypi.org/project/PyAutoGUI/
    https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py

---

# Open Software

    musicbee:        Music Bee
    cloudmusic:      网易云音乐PC版
    keepdisplayon:   Keep Screen On

---

Default port 8836, you can define port with argument.
</pre>
'''
    yield info.encode('utf-8')


# ═══════════════════════════════════════════════


def init_server(port=8836):
    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/api', rest_api)

    # Launch a basic server
    httpd = make_server('', port, dispatcher)
    print(f'Serving on port {port}...')
    httpd.serve_forever()


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    port = 8836 if len(sys.argv) == 1 else sys.argv[1]
    init_server(port)
