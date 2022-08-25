#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

try:
    from .pd2excel import main
except ImportError:
    from pd2excel import main

import fire

# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # here = os.path.abspath(os.path.dirname(__file__))
    # file = os.path.join(here, '招聘报表.xls')

    # main(file)
    fire.Fire(main)
