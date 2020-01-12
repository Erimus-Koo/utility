#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 中文数字转阿拉伯数字


def swap_kv(dic):
    r = {}
    for k, v in dic.items():
        for i in v:
            r.setdefault(i, k)
    return r


cnNum = {1: '一壹', 2: '二贰两', 3: '三叁', 4: '四肆', 5: '五伍',
         6: '六陆', 7: '七柒', 8: '八捌', 9: '九玖'}
cnNum = swap_kv(cnNum)

cnUnit = {1: '十拾', 2: '百佰', 3: '千仟', 4: '万萬', 8: '亿億',
          12: '兆', 16: '京', 20: '垓', 24: '秭', 28: '穰',
          32: '沟', 36: '涧', 40: '正', 44: '载'}
cnUnit = swap_kv(cnUnit)
# [print(k, v) for k, v in cnNum.items()]
# [print(k, v) for k, v in cnUnit.items()]


def cnNum2Int(s):
    crtNum = 0  # 当前总值
    base = 0    # 当前不含单位的底数
    k_base = 0  # 千级底数
    for i in s:
        if i.isdigit():
            base = base * 10 + int(i)
        else:
            base = cnNum.get(i, base)
        if i in cnUnit:
            if cnUnit[i] > 3:  # 超过千位
                crtNum += (k_base + base) * (10**cnUnit[i])
                base, k_base = 0, 0
            else:  # 千位及以下
                if cnUnit[i] == 1:  # 十前面没有序数的特殊处理
                    base = max(base, 1)
                k_base += base * (10**cnUnit[i])
                base = 0
        # print(i, base, k_base, crtNum)  # debug
    return crtNum + k_base + base


if __name__ == "__main__":

    for s in [
        '一百零五万零二十五',
        '十',
        '十万',
        '贰拾萬',
        '两千五百万零十一',
        '五百零三亿四万五千六百八十七',
        '56万2千零1',
        '1234',
        '12三四',
    ]:
        print(f'{s} ---> {cnNum2Int(s)}')
