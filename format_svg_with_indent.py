#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
# SVG Formatter Script for Draw.io Exports

Draw.io exports SVG files as a single line, which is hard to manage with Git.
This script formats those SVGs with indents for better readability and Git.

Add it in your project and use it in Git hooks (e.g., `pre-commit`)

```sh
#!/bin/bash
python path/to/this.py
```
'''

import html
import os
import re
from xml.dom.minidom import parseString

# ═══════════════════════════════════════════════


def format_xml(xml_string):
    # Parse the XML string into a DOM structure
    dom = parseString(xml_string)
    # Format the XML with indentation
    formatted_xml = dom.toprettyxml(indent="  ")
    return formatted_xml


def format_xml_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        xml_string = f.read()

        # If rows greater than 4, it's formatted.
        rows = len(xml_string.splitlines())
        # print(f'{rows = }')
        if rows > 5:
            return

    # Make a backup
    path, fn = os.path.split(file)
    bkp_file = os.path.join(path, f'.${fn}.bkp')
    os.rename(file, bkp_file)  # backup, ignore .bkp in Git plz

    # Format svg's xml
    formatted_xml = format_xml(xml_string)

    # Draw.io saves diagram's xml in svg content attribute as escaped string,
    # split it in multi-lines with indent too.
    content = re.search(r'(?ms)content="(.*?)"', formatted_xml).group(1)
    content_formatted = html.unescape(content.strip())
    content_formatted = format_xml(content_formatted)
    content_formatted = html.escape(content_formatted)
    # print(f'{content_formatted = }')
    formatted_xml = formatted_xml.replace(content, content_formatted)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(formatted_xml)


def read_all_files_in_project(root):
    for path, dirs, files in os.walk(root):  # read all files
        for fn in files:
            if fn.lower().endswith('.svg'):
                file = os.path.join(path, fn)  # full path
                format_xml_file(file)


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    file = r'G:\Downloads\012_Must-Want.svg'
    format_xml_file(file)

    # I often put this in project_root/utils
    # here = os.path.abspath(os.path.dirname(__file__))
    # root, _ = os.path.split(here)
    # read_all_files_in_project(root)
