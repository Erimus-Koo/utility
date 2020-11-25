#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import pandas as pd
import json

# ═══════════════════════════════════════════════


def read_excel(source,              # 要读取的excel文件
               sheet=None,          # sheet None为全部 可以传入str或list
               header=0,            # 标题前隔开几行 0=第一行是标题
               return_type='json',  # 返回格式 默认json 不指定为直接返回df
               df_format=None,      # 格式化字段
               **kwargs):
    '''
    读取指定excel，并返回数据。

    可以返回指定sheet的内容，或者返回全部sheet（以字典方式）。
    只有一个sheet也返回该sheet内容。

    返回数据默认是每行一个json。也可以直接把各个sheet以dataframe形式返回。
    '''

    # sheet_name = None 以字典返回所有表
    df = pd.read_excel(source, sheet_name=None, header=header, **kwargs)

    # 格式化sheet为数组
    if isinstance(sheet, str):
        sheet = [sheet]

    # 剔除无效表
    if sheet is not None:  # 指定表
        # 仅保留指定表的内容（拆开写避免df.copy过大）
        unneed = [sn for sn in df if sn not in sheet]
        [df.pop(sn) for sn in unneed]
    else:
        # 删除空表
        empty_sheet = [k for k, v in df.items() if v.empty]
        [df.pop(k) for k in empty_sheet]

    # 格式化数据
    if df_format is not None:
        df.format = df_format

    # 清洗数据
    for sheet_name, data in df.items():
        data.fillna('', inplace=True)  # 用空值替换错误值
        if return_type == 'json':  # 转为json
            df[sheet_name] = json.loads(data.to_json(orient='records'))

    # if len(df) == 1:  # 只有一个表则返回内容
    #     return list(df.values())[0]
    # else:  # 如果有多个表则返回字典
    print('---\nRead excel result:')
    [print(f'{sheet}: {len(data)} rows') for sheet, data in df.items()]
    return df


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    read_excel()

    # format sample
    # df.format = {
    #     'a': '{:,.1f}'.format,
    #     'b': '{:,.0f}'.format,
    #     'c': '{:.1%}'.format,
    #     'd': '{:d}'.format,
    #     'e': '{:s}'.format,
    # }
