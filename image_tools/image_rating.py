#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 查看圖片評級

import re

# ═══════════════════════════════════════════════


# MicrosoftPhoto Rating 如果通過Explorer調整，1星和其他星數互轉會有問題。
# 1星數值1佔1位，其他星佔兩位，可能會導致文件驗證錯誤。
# 所以放棄強制修改(改動後會無法再編輯)，盡量用Bridge查看修改。
# 只能修改等級，原本未打星的文件無法設置等級。
def read_rating(file, modify_rating=None):
    rDict = {1: ' 1', 2: '25', 3: '50', 4: '75', 5: '99'}  # xmp:MicrosoftPhoto
    modified = False

    def str2int(string):
        return int(re.findall(b'\d+', string)[0])

    with open(file, 'rb') as old:
        f = old.read()

    r, msr = None, None
    if b'xmp:Rating' in f:
        try:  # modify by Adobe Bridge
            r_str = re.findall(b'xmp:Rating="\d+?"', f)[0]
            r = str2int(r_str)
            if modify_rating is not None and modify_rating != r:
                r = modify_rating
                f = f.replace(r_str, b'xmp:Rating="%b"'
                              % str.encode(str(r)))
                print('xmp:Rating="%s" -> "%s"' % (str2int(r_str), r))
                modified = True
        except Exception:  # modify by Explorer
            r_str = re.findall(b'xmp:Rating>\d+?</', f)[0]
            r = str2int(r_str)
            if modify_rating is not None and modify_rating != r:
                r = modify_rating
                f = f.replace(r_str, b'xmp:Rating>%b</'
                              % str.encode(str(r)))
                print('xmp:Rating="%s" -> "%s"' % (str2int(r_str), r))
                modified = True

    if b'MicrosoftPhoto:Rating' in f:
        try:  # modify by Adobe Bridge
            msr_str = re.findall(b'MicrosoftPhoto:Rating="[ 0-9]{2}"', f)[0]
            msr = str2int(msr_str)
            # print(msr_str, msr)
            if int(rDict[r]) != msr:
                f = f.replace(msr_str, b'MicrosoftPhoto:Rating="%b"'
                              % str.encode(rDict[r]))
                print('MicrosoftPhoto:Rating="%s" -> "%s"' % (msr, rDict[r]))
                modified = True
        except Exception:  # modify by Explorer
            msr_str = re.findall(b'MicrosoftPhoto:Rating>[ 0-9]{2}</', f)[0]
            msr = str2int(msr_str)
            # print(msr_str, msr)
            if int(rDict[r]) != msr:
                f = f.replace(msr_str, b'MicrosoftPhoto:Rating>%b</'
                              % str.encode(rDict[r]))
                print('<MicrosoftPhoto:Rating>%s -> %s' % (msr, rDict[r]))
                modified = True

    if modified:
        with open(file, 'wb') as new:
            new.write(f)

    return r or 0


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    file = 'D:/Downloads/photo backup/test.jpg'
    rating = read_rating(file, 5)
    print(rating)
