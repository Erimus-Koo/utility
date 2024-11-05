#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import pandas as pd
import numpy as np
import logging as log
import os
import re
import datetime
import time
from pprint import pp

# ═══════════════════════════════════════════════
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.max_columns', 10)  # None=unlimited
# pd.set_option('display.max_rows', 10)  # None=unlimited
# pd.options.display.float_format = '{:,.1f}'.format  # set float format
# ═══════════════════════════════════════════════
excel_start_time = datetime.datetime(1900, 1, 1, 0, 0, 0)
DEFAULT_FONT = {
    'font_name': 'Microsoft Yahei',
    'text_wrap': True,
    'valign': 'vcenter',
}
MONOSPACE = {
    'font_name': 'Courier New',
    'bold': True,
    'valign': 'vcenter',
}

# 数字格式
NUM_DICT = {  # type desc: number format
    'int': '###0',
    'float': '#,##0.00',
    'percentage': '0.00%',
    'datetime': 'yyyy-mm-dd hh:mm:ss',
    'date': 'yyyy-mm-dd',
    'time': 'hh:mm:ss',
}

# letter width
LETTER_WIDTH = 1.25
DL = '\n' + '-' * 30 + '\n'
# ═══════════════════════════════════════════════ archive

# col转datetime 并转为excel中的数字型日期
# def convert_col_to_datetime(df, col):
#     df[col] = pd.to_datetime(df[col])
#     print(f'[{col}] {df[col].dtype = }')
#     df[col] = df[col] - excel_start_time
#     df[col] = df[col].dt.days + df[col].dt.seconds / 86400
#     [log.debug(f'{cell = }') for cell in df[col]]
#     if all([c % 1 == 0 for c in df[col] if c and c == c]):
#         datetime_dict[col] = 'date'
#     elif all([c < 1 for c in df[col] if c and c == c]):
#         datetime_dict[col] = 'time'
#     else:
#         datetime_dict[col] = 'datetime'
#     log.debug(f'[{col}] --> {datetime_dict[col]}')

# ═══════════════════════════════════════════════


def deal_with_sheet(writer, sheet_name, data, index=None):
    # print(f'{DL}{sheet_name = }')
    # valid sheetname
    sheet_name = re.sub(r'[\\\/\*\?\:\[\]]', '_', sheet_name)

    # 处理导入的数据
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        raise f'DataError: {data}'

    # 处理重名列
    if len(list(df.columns)) != len(set(df.columns)):
        print(f'{DL}包含重名的列!!!\n{df.columns = }')
        raise

    r = {}

    # 填充错误值
    df.fillna('', inplace=True)

    # 自动转格式
    log.debug(f'{DL}Auto convert dtype{DL}')
    src_dtypes = list(df.dtypes)
    df = df.convert_dtypes()
    for i, col in enumerate(df.columns):
        if str(src_dtypes[i]) != str(df[col].dtype):
            log.debug(f'{col:<15s} {src_dtypes[i]} --> {df[col].dtype}')

    # 如果index是递增数字 则不输出index
    log.debug(f'{DL}Check index{DL}')
    if index is None:
        index = True
        if any((pd.api.types.is_integer_dtype(df.index),
                all(str(idx).isdigit() for idx in df.index))):
            df_index = sorted(df.index.tolist())
            # 相邻的两个递增index的差 大部分为1时 认为是自动生成的递增index
            if ([b - a for a, b in zip(df_index[:-1], df_index[1:])].count(1)
                    > len(df_index) / 2):
                log.debug('>>> ignore index')
                index = False
    if index:
        df.reset_index(inplace=True)  # 把index转为正常列

    # 创建分表 (必须在确定了数据之后，也就是index重置之后)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    '''
    日期时间加格式有两种方式
    1. 转为字符串，不然后面设不上格式。缺点是会丢失应有的格式。
    2. 计算为excel起始日期的天数，然后加num format。
       缺点是excel对时间日期格式要求很严格，会触发很多意外的类型错误。

    最后决定用方式1，这样需要处理：
    1. 把真正的日期时间类型也转为字符串（不然没有样式）
    2. 把看上去像数字类型的字符串标记出来
    '''
    log.debug(f'{DL}Convert all unknown dtype to string{DL}')
    # datetime_dict = {}
    for col_i, col in enumerate(df.columns):
        r.setdefault(col, {'col': col})
        r[col]['old'] = df[col].dtype
        if not any((
                pd.api.types.is_numeric_dtype(df[col]),
                pd.api.types.is_string_dtype(df[col]),  # object --> true
        )):  # or pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype(str)  # --> object
            if all([is_int(c) for c in df[col] if c != ''][:-1]):
                df[col] = df[col].apply(lambda x: x[:-2]
                                        if x.endswith('.0') else x)
                df[col] = df[col].astype(int, errors='ignore')
                print(f'{df[col] = }')
                convert_info = '--> str --> int'
            elif all([is_float(c) for c in df[col] if c != ''][:-1]):
                df[col] = df[col].astype(float, errors='ignore')
                convert_info = '--> str --> float'
            else:
                convert_info = '--> str'
        else:
            convert_info = ''
        log.debug(f'{col:<15s} {df[col].dtype} {convert_info}')

    # 把表作为工作表
    worksheet.add_table(
        0, 0, df.shape[0], df.shape[1] - 1, {
            'columns': [{
                'header': col
            } for col in df.columns],
            'style': 'Table Style Medium 1'
        })
    worksheet.set_default_row(hide_unused_rows=False)  # 不要自动隐藏

    # header format
    header_format = DEFAULT_FONT.copy()
    header_format.update({'bold': True, 'valign': 'top'})
    header_format = workbook.add_format(header_format)
    worksheet.set_row(0, None, header_format)

    # 自动设定格式和宽度
    log.debug(f'{DL}Auto column width{DL}')
    column_width_dict = {}
    for col_i, col in enumerate(df.columns):
        log.debug(f'{DL}[{col}]\n{df[col].loc[:3]}')
        data_type = 'str'  # default

        # log.debug(f"[{col}]\n{[c for c in df[col] if c != '']}\n{[is_int(c) for c in df[col] if c != '']}")
        if any((pd.api.types.is_integer_dtype(df[col]),
                all([is_int(c) for c in df[col] if c != ''][:-1]))):  # 整数
            data_type = 'int'
        elif any((pd.api.types.is_float_dtype(df[col]),
                  all([is_float(c) for c in df[col] if c != ''][:-1]))):  # 小数
            data_type = 'float'
            if col.endswith(('率', '百分比', '占比')):
                data_type = 'percentage'

        # 看起来像数字（日期时间等）需要使用monospace的
        elif all([is_num_like(c) for c in df[col] if c != ''][:-1]):
            data_type = 'mono'

        # 根据 date type 设置格式
        log.debug(f'{DL}>>>>> [{col}] {df[col].dtype} --> {data_type} <<<<<')
        r[col]['new'] = data_type

        this_fmt = DEFAULT_FONT.copy()
        if data_type in NUM_DICT or data_type in ['mono']:
            log.debug(f'format: {NUM_DICT.get(data_type)}')
            this_fmt = MONOSPACE.copy()
            if data_type in ['mono']:
                this_fmt['align'] = 'center'
            if NUM_DICT.get(data_type):
                this_fmt['num_format'] = NUM_DICT[data_type]

        # 计算列宽
        header_len = (real_len(col) +
                      2) / 2  # add some space for filter button
        if data_type in NUM_DICT:
            if data_type == 'float':
                max_len = df[col].map(lambda x: str_round(x, 2)).map(str).map(
                    len).max()
            elif data_type == 'percentage':
                max_len = df[col].map(lambda x: str_round(x, 4)).map(str).map(
                    len).max()
            else:
                max_len = df[col].map(str).map(len).max()
        else:
            max_len = str_most_len(df[col].map(str).map(real_len))
            if max_len < 8:
                this_fmt['align'] = 'center'

        max_len = max(max_len, header_len)
        col_width = min(max_len * LETTER_WIDTH, 50)
        r[col]['width'] = col_width
        col_name = excel_col_index_to_name(col_i)
        r[col]['idx'] = col_name
        fmt = workbook.add_format(this_fmt)
        worksheet.set_column(f'{col_name}:{col_name}', col_width, fmt,
                             {'hidden': 0})
        log.debug(f'[{col}]\n{col_name = } | {max_len = } | {col_width = }\n'
                  f'{this_fmt}{DL}')
        column_width_dict[col] = col_width

    # print result
    # [log.debug(f'{v:>5.2f} | {k}') for k, v in column_width_dict.items()]
    rdf = pd.DataFrame(list(r.values()))
    rdf = rdf[['col', 'idx', 'old', 'new', 'width']]
    rdf.set_index('col', inplace=True)
    log.debug(f'{DL}{rdf}{DL}')

    # 设定行高避免过高
    log.debug(f'{DL}Auto row height{DL}')
    for row_i, row in df.iterrows():
        max_lines = 0
        # 表格标题
        for col in df.columns:
            lines = real_len(str(col)) * LETTER_WIDTH / column_width_dict[col]
            max_lines = max(max_lines, lines)
        if max_lines > 3:
            worksheet.set_row(0, 50, header_format)  # 50大概是3行行高
        # 表格内容
        for col in df.columns:
            lines = (real_len(str(row[col])) * LETTER_WIDTH /
                     column_width_dict[col])
            max_lines = max(max_lines, lines)
        if max_lines > 3:
            worksheet.set_row(row_i + 1, 50)  # 50大概是3行行高
    return writer


def save_excel(data, output, *, index=None):
    if isinstance(data, pd.DataFrame) or isinstance(data, list):
        data = {'Sheet1': data}

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    for sheet_name, df in data.items():
        writer = deal_with_sheet(writer, sheet_name, df, index=index)

    writer.close()
    print(f'💾 Saved: {output}')


# ═══════════════════════════════════════════════


def excel_col_index_to_name(col_index):  # col_index starts with 0
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    col_index += 1
    while col_index:
        col_index, rem = divmod(col_index - 1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)


def real_len(string):
    if '\n' in string:
        return max([(len(line) + len(line.encode('utf-8'))) // 2
                    for line in string.split('\n')])
    # 中文返回2个宽度
    return (len(string) + len(string.encode('utf-8'))) // 2


def str_round(string, length):
    string = str(string)
    if '.' in string:
        return string[:string.index('.') + length + 1]
    else:
        return string


def str_most_len(array):
    # 传入字符串宽度数组 传出中等偏宽的具体宽度
    array = [i for i in array if i]
    med = 0
    for _ in range(3):
        med = np.median([i for i in array if i >= med])
    return med


def is_int(cell):
    try:
        cell_f = float(cell)
        cell_i = int(cell_f)
    except (TypeError, ValueError):
        return False
    else:
        return cell_f == cell_i


def is_float(cell):
    try:
        float(cell)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_num_like(cell):
    # 获取cell内容 如果是时间格式 返回对应的sting 不是时间格式返回否
    if isinstance(cell, str):
        r = re.match(r'[\d\-/: \.]+', cell)
        if r and r.group() == cell:
            return True
    else:
        log.debug(f'{cell = } not str')


# ═══════════════════════════════════════════════


def main(input_content):
    if all(
        (os.path.isfile(input_content), input_content.endswith(
            ('xls', 'xlsx')))):
        wb = pd.ExcelFile(input_content).book
        if len(wb.sheetnames) > 1:
            log.warning(f'Single sheet support only, bye.')
            return
        sheet_name = wb.sheetnames[0]
        log.info(f'{wb.sheetnames = }')
        df = pd.read_excel(input_content, header=None)
        header, prev_idx, prev = 0, 0, []
        for ri, row in df.iterrows():
            # print(f'{ri = } {row = }')
            if ri == 0:
                prev_idx, prev = ri, [h for h in row if h == h]
                continue
            if len(row) == len(prev) and all([h == h for h in prev]):
                header = prev_idx
                print(f'Auto detect {header = }')
                break
            elif len(row) > len(prev):
                prev_idx, prev = ri, [h for h in row if h == h]
        else:
            print(f'Auto detect header failed. {header = }')

        df = pd.read_excel(
            input_content,
            header=[header],
        )
        file, ext = os.path.splitext(input_content)
        output = f'{file}_formatted.xlsx'
        save_excel(df, output, index=None, sheet_name=sheet_name)


def test_multi_sheet():
    df1 = pd.DataFrame([{'id': i, 'name': 'name'} for i in range(100)])
    df2 = pd.DataFrame([{'id': f'-{i}', 'name': 'name'} for i in range(100)])
    here = os.path.abspath(os.path.dirname(__file__))
    output = os.path.join(here, f'test_multi_sheet.xlsx')
    save_excel({'s1': df1, 's2': df2}, output)
    os.system(f'open {output}')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    log.basicConfig(level=log.DEBUG,
                    format=('[%(asctime)s] %(message)s'),
                    datefmt='%m-%d %H:%M:%S')

    here = os.path.abspath(os.path.dirname(__file__))
    file = '招聘报表.xls'
    file = 'cv2021-08-30.xlsx'
    # file = 'moka_client_pretty.xlsx'

    # main(os.path.join(here, file))

    test_multi_sheet()
