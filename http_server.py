#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 以本机 ip 启动 http server

import http.server
import os
import socket
import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

import fire
from art import tprint

# ═══════════════════════════════════════════════


def http_server_old(root=None, port=80):
    if root is None:
        root = os.getcwd()

    # get host ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f'{ip = }')

    valid = True
    for seg in ip.split('.'):
        if not seg.isdigit():
            valid = False
    if not valid:
        raise ValueError(f'Error: {ip}')

    tprint(ip, 'wizard')

    python = 'python' if os.name == 'nt' else 'sudo python3'  # mac need sudo sometime
    cmd = f'{python} -m http.server {port} --directory "{root}" --bind {ip}'
    print(f'{cmd = }')
    os.system(cmd)


# ═══════════════════════════════════════════════


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        self.root_dir = directory
        super().__init__(*args, directory=directory, **kwargs)

    def translate_path(self, path):
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.root_dir, relpath)
        print(f'{fullpath = }')
        return fullpath


def make_handler(root_dir):

    def handler(*args, **kwargs):
        return CustomHTTPRequestHandler(*args, directory=root_dir, **kwargs)

    return handler


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def http_server(root_dir=None):
    if root_dir is None:
        root_dir = os.getcwd()
    print(f'{root_dir = }')

    ip = get_host_ip()
    tprint(ip, 'wizard')

    cert_path = '/Users/erimus/Library/Application Support/mkcert'
    cert = f'{cert_path}/rootCA.pem'
    key = f"{cert_path}/rootCA-key.pem"
    print(f'{cert = }')
    print(f'{key = }')

    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

        def do_GET(self):
            self.path = self.path.lstrip('/')
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Change the directory to the one where your 'moats_translate_dict.csv' file is located
    os.chdir(root_dir)

    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    my_server = http.server.HTTPServer(("", 4443), handler_object)

    # For SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert, keyfile=key)

    my_server.socket = ssl_context.wrap_socket(my_server.socket,
                                               server_side=True)

    my_server.serve_forever()


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    fire.Fire(http_server)
