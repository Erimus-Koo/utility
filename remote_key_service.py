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

# ═══════════════════════════════════════════════
pyautogui.FAILSAFE = False  # screen off keep working
# ═══════════════════════════════════════════════

class PathDispatcher:
    def __init__(self):
        self.pathmap = { }

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = { key: params.getvalue(key) for key in params }
        handler = self.pathmap.get((method,path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function


# ═══════════════════════════════════════════════


def remote_key(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']
    if 'key' not in environ['params']:
        msg = 'No Param "key": {environ["params"]}'
    else:
        key = environ['params']['key'].lower()
        # play key on local
        if '_' in key:
            keys = key.split('_')
            msg = f'HOTKEY: {keys}'
            pyautogui.hotkey(*keys)
        else:
            msg = f'PRESS: {key}'
            pyautogui.press(key)

    print(msg)
    yield f'[{os.getpid()}] {msg}\n'.encode('utf-8')


# ═══════════════════════════════════════════════


def notfound_404(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    info = '''
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

Default port 8836, you can define port with argument.

'''
    yield info.encode('utf-8')


# ═══════════════════════════════════════════════


def init_server(port):
    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/send', remote_key)

    # Launch a basic server
    httpd = make_server('', port, dispatcher)
    print(f'Serving on port {port}...')
    httpd.serve_forever()


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    port = 8836 if len(sys.argv) == 1 else sys.argv[1]
    init_server(port)
