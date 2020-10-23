#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 简化pandas的一些常用命令，简化日常使用二维表格时的增删等操作。

import pandas as pd
from util.print_table import printTable

# ═══════════════════════════════════════════════


class Pandas():
    # 新建空表
    def __init__(self, headers=None, columns=None, df=None):
        self.columns = columns or headers or []
        if df is None:
            self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = df
            self.columns = df.columns.values
        self.format = {}

    def __repr__(self):
        if self.format:
            return self.df.to_string(formatters=self.format)
        else:
            return repr(self.df)

    # 重定义列 排序 插入
    def set_column(self, columns):
        assert isinstance(columns, list)
        temp_df = pd.DataFrame()
        for col in columns:
            if col in self.columns:
                temp_df[col] = self.df[col]
            else:
                temp_df[col] = '-'
        self.df = temp_df
        self.columns = self.df.columns
    set_header = set_column

    def add_column(self, *columns):
        self.set_column(list(self.columns) + list(columns))

    def del_column(self, *columns):
        temp_columns = list(self.columns)
        [temp_columns.remove(col) for col in columns]
        self.set_column(temp_columns)

    def add_row(self, *rows, columns=None, index=None):
        # 处理新增的列
        for row in rows:
            if isinstance(row, dict):
                for k in row.keys():
                    if k not in self.columns:
                        self.add_column(k)
        columns = columns or self.columns
        index = [index] if isinstance(index, str) else index
        new_df = pd.DataFrame([*rows], index=index, columns=columns)
        if index:
            self.df = self.df.append(new_df)
        else:
            self.df = self.df.append(new_df, ignore_index=True)

    def sort(self, column_name, reverse=False):
        self.df = self.df.sort_values(by=column_name, ascending=(not reverse))

    def tolist(self, fmt=False, index=False, header=True):
        df = self.df.copy()
        df.fillna('', inplace=True)
        column_name = list(self.columns)
        if index:  # 如果需要包括index
            df = df.reset_index()
            column_name = [''] + column_name  # index的列名
        table = df.values.tolist()
        if fmt:
            for ri, row in enumerate(table):
                for ci, col in enumerate(row):
                    cname = column_name[ci]
                    if cname in self.format:
                        table[ri][ci] = self.format[cname](col)
        if header:
            table = [column_name] + table
        return table

    def print_table(self, index=True, **kwargs):
        printTable(self.tolist(fmt=True, index=True, header=True),
                   has_header=True, **kwargs)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    df = Pandas(['b', 'c', 'a'])
    print(f'\n---\nCreate empty DataFrame (with headers)\n{df}')
    print(dir(df))

    df.add_row([1, 2, 3])  # 添加单行
    df.add_row([4, 5, 6], [7, 8, 9])  # 添加多行
    print(f'\n---\nAppend rows\n{df}')

    df.add_row({'a': 9, 'b': 7, 'c': 8}, index='dict')  # 添加指定列的行
    df.add_row({'a': 9, 'b': 7, 'nc': 88}, index='new col')  # 添加含新增的列的行
    print(f'\n---\nAppend rows (by dict and has index)\n{df}')

    df.set_column(['a', 'b', 'c'])  # 重设列 用来排序（可增删列）
    print(f'\n---\nReset columns (sort)\n{df}')

    df.add_column('d', 'e')  # 添加列（*args可多列）
    print(f'\n---\nAdd columns ("d")\n{df}')

    df.del_column('d')  # 删除列（*args可多列）
    print(f'\n---\nDelete columns\n{df}')

    df.sort('a', reverse=True)  # 排序
    print(f'\n---\nSort by col "a" reversed\n{df}')

    # 可以仅设置部分列
    df.format = {
        'a': '{:,.1f}'.format,
        'b': '{:,.0f}'.format,
        'c': '{:.1%}'.format,
    }
    print(f'\n---\nFomart Data\n{df.format = }\n{df}')

    print(f'\n---\nConvert to List')  # 转为列表
    print(f'{df.tolist() = }')

    print(f'\n---\nPrint Table')  # 打印表格
    df.print_table(group='a')  # 可传**kwargs给printTable
