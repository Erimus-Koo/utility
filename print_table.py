#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 打印二维表格

import copy
from prettytable import PrettyTable
from erimus.toolbox import FS, CSS

# ═══════════════════════════════════════════════


def no_anis(string): return re.sub(r'\x1b[\[\d]+m', '', string)


def is_num(string):
    if isinstance(string, (int, float)):
        return True
    string = string.replace(',', '')
    string = string[:-1] if string.endswith('%') else string
    if string.isdigit():
        return True
    try:
        float(string)
        return True
    except:
        pass


# 打印表格
def printTable(
    table,                      # 二维数组
    has_header=True,            # table第一行是否是标题
    header=None,                # 表标题
    group=None,                 # 传入列名 该列如果连续行内容一致 则组合显示
    thousand_separator=True,    # 千位分隔符
    zero=None,                  # 0的替代字符
    frame_color=None,           # 边框颜色
    header_color=None,          # 标题颜色
    column_color=None           # 数组 各列的颜色
):
    if not table:  # 表格为空
        return

    col_num = len(table[0])  # 获取列数

    # 打印超大表格前提示
    if len(table) > 500:
        print(FS.warning('THE TABLE IS TOO BIG!!!'))
        print(FS.warning(f'Row: {len(table)} | Column: {col_num}'))
        print(FS.warning('Press enter to continue...'))
        input()

    table = copy.deepcopy(table)  # 深拷贝 避免影响原表

    # 修复表格的一些基本问题
    for ri, row in enumerate(table):
        if isinstance(row, tuple):  # sorted产生的元组 自动转换
            table[ri] = list(row)
        if isinstance(row, dict):
            table[ri] = list(row.values())
        if len(row) < col_num:  # 补全缺少的列
            table[ri] = (table[ri] + [''] * col_num)[:col_num]

    # 没标题的话补完标题
    if not header:  # create header
        if has_header:  # 是否认为第一行是标题
            header, table = table[0], table[1:]
            tb = PrettyTable(header)
        else:
            header = [str(h) for h in range(col_num)]  # set align need header name
            tb = PrettyTable(header)
            tb.header = False
    else:
        tb = PrettyTable(header)

    # 处理合并显示
    insert_hr = False
    hr_row = ['<hr>'] + [''] * (col_num - 1)  # 上下增加横线
    insert_line = 0
    this_value = None
    if group:
        group_column_index = header.index(group)
        for row_idx, row in enumerate(table[:]):  # 以行为单位调整表格
            if this_value == row[group_column_index]:
                table[row_idx + insert_line][group_column_index] = ''
            else:
                this_ri = row_idx + insert_line
                this_value = row[group_column_index]
                # 不加横线的条件
                if (row_idx == 0  # 第一行
                        # 因为子标题上下会自动加横线 所以它和下一行不加
                        or str(row[0]).startswith('###')  # 子标题
                        or str(table[this_ri - 1][0]).startswith('###')  # 下一行
                        ):
                    continue
                insert_hr = True
                table = table[:this_ri] + [hr_row] + table[this_ri:]
                insert_line += 1

    # 处理子表格标题（确保多组表格列宽一致）
    insert_line = 0
    for row_idx, row in enumerate(table[:]):  # 以行为单位调整表格
        if isinstance(row[0], str) and row[0].startswith('###'):  # 标题行
            insert_hr = True
            table = (table[:row_idx + insert_line]
                     + [hr_row] + [hr_row]
                     + [[row[0].strip('# ')] + row[1:]]
                     + [hr_row]
                     + table[row_idx + insert_line + 1:])
            insert_line += 3

    # 边框样式
    if frame_color is None:
        frame_color = 'red'
    tb.vertical_char = CSS('|', frame_color)
    tb.horizontal_char = CSS('-', frame_color)
    tb.junction_char = CSS('+', frame_color)

    # 表格的默认对齐
    for i, c in enumerate(table[0]):
        c = str(c).replace(',', '').replace('.', '').replace('%', '')
        if is_num(c):
            align = 'r'
        else:
            align = 'l'
        tb.align[header[i]] = align

    # 标题颜色
    header_color = header_color or 'white'
    header = [CSS(c, f'bd{header_color}') for c in header]

    # 表格颜色
    for row_idx, row in enumerate(table):  # 调整单元格
        colored_row = []
        for col_idx, cell in enumerate(row):
            percent_mark = ''
            if isinstance(cell, str) and cell.endswith('%'):
                cell = cell[:-1]
                percent_mark = CSS('%', 'r')
            if zero is not None and cell == 0:  # 替换0的显示字符
                cell = zero
            # set color for cell
            if column_color:  # 如果设置过整列颜色
                _color = column_color[col_idx]
            else:  # 默认颜色
                _color = 'magenta' if is_num(cell) else 'white'
            # 增加千位分隔符
            if thousand_separator and isinstance(cell, int):
                cell = f'{cell:,d}'
            if thousand_separator and isinstance(cell, float):
                cell = f"{cell:,.0f}{str(cell)[str(cell).index('.'):]}"
            colored_row.append(CSS(cell, _color) + percent_mark)

        tb.add_row(colored_row)

    # 把插入的横线符号显示为横线
    if insert_hr:
        rows = str(tb).split('\n')
        rows = [rows[0] if '<hr>' in row else row for row in rows]
        tb = '\n'.join(rows)

    print(tb)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    tb = [
        [1, 2, 3],
        [1, 2, 3],
        [4, '51.1%', 6000],
        [4, '52.2%', 6001],
        [4, '53.3%', 6002],
        ['### table 2'],
        ['name', 8.1, -9],
        ['name', 8.2, 9],
    ]

    def title(x): return print(f"\n{x.center(30, '=')}")

    title('NORMAL'.center(30, '='))
    printTable(tb, header=['a', 'b', 'c'])

    title('GROUP'.center(30, '='))
    printTable(tb, header=['a', 'b', 'c'], group='a')

    title('NO HEADER'.center(30, '='))
    printTable(tb, has_header=0)

    title('UNSET HEADER'.center(30, '='))
    printTable(tb)
