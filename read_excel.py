#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import pandas as pd
import json

# ═══════════════════════════════════════════════


def read_excel(source, sheet=None, header=0, return_type='json', **kwargs):
    '''
    读取指定excel，并返回数据。

    可以返回指定sheet的内容，或者返回全部sheet（以字典方式）。
    只有一个sheet也返回该sheet内容。

    返回数据默认是每行一个json。也可以直接把各个sheet以dataframe形式返回。
    '''

    # sheet_name = None 以字典返回所有表
    df = pd.read_excel(source, sheet_name=None, header=header, **kwargs)

    # 剔除无效表
    if sheet is not None:  # 指定表
        df = {sheet: df[sheet]}
    else:
        # 删除空表
        empty_sheet = []
        for k, v in df.items():
            if v.empty:
                empty_sheet.append(k)
        [df.pop(k) for k in empty_sheet]

    # 清洗数据
    for k, v in df.items():
        v.fillna('', inplace=True)  # 用空值替换错误值
        if return_type == 'json':  # 转为json
            df[k] = json.loads(v.to_json(orient='records'))

    if len(df) == 1:  # 只有一个表则返回内容
        return list(df.values())[0]
    else:  # 如果有多个表则返回字典
        return df


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    read_excel()
