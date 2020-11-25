#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 给excel模板填充数据

import time
import os
import shutil
from .write import WriteExcel

# ═══════════════════════════════════════════════


def fill_excel_module(*, module, data, output=None):
    '''
    module  模板文件的完整路径。使用文件第一个sheet作为模板，填充数据。
    data    字典。{sheet_name:[[row1cell1,cell2,...],[row2...],...]}
    '''

    # 复制为新文件
    if output is None:
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        output = module.replace('_模板.', f'_{now}.')
    shutil.copy(module, output)  # shutil对路径比较宽容
    print(f'Output: {output}\n')

    # 初始化excel
    md = WriteExcel(output)

    # 获取模板基本信息
    module_sheet = md.wb.Sheets(1)
    print(f'Module Sheet Name: {module_sheet.Name}')

    main_table = md.wb.Sheets(1).ListObjects(1)  # 一般模板上只有一个表
    hdr_row = main_table.HeaderRowRange.Row  # 标题行所在行数
    print(f'Header at row: {hdr_row}')
    header = main_table.HeaderRowRange.Value[0]  # 标题内容
    print(f'{header = }')

    module_rows_total = main_table.DataBodyRange.Rows.Count
    print(f'Module table rows total: {module_rows_total}')

    # 含公式 自动计算的列
    formula_columns = [h for i, h in enumerate(header)
                       if main_table.DataBodyRange
                       .Columns(i + 1).Rows(1).HasFormula]
    print(f'Columns with formula: {formula_columns}')

    # 新数据填入
    for sheet_name, rows in data.items():
        # 复制表
        print(f'\nDuplicate sheet: {sheet_name}')
        md.copy_sheet(src=module_sheet.Name, new=sheet_name)

        # 调整表格有效行数为目标行数
        add_rows = len(rows) - module_rows_total
        print(f'Total {len(rows)} rows (need {add_rows})')
        if add_rows > 0:
            md.insert(sheet=sheet_name, row=f'{hdr_row+1}:{hdr_row+add_rows}')
        elif add_rows < 0:
            md.delete(sheet=sheet_name, row=f'{hdr_row+1}:{hdr_row-add_rows}')

        # 构成整张表的数据
        print(f'Adding data to table')
        # 按列贴入内容 data没有的列就跳过以保留公式
        for ci, key in enumerate(header):
            this_column = md.wb.Sheets(sheet_name).ListObjects(1)\
                .DataBodyRange.Columns(ci + 1)
            if key not in formula_columns:  # 跳过含公式的列
                # 修改列数据
                this_column.Value = [[row.get(key)] for row in rows]

    # 删除模板表
    md.delete_sheet(module_sheet.Name)

    # 选择第一张表
    md.wb.Sheets(1).Select()

    # 保存
    md.save_and_close()


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    here = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(here, '商品总表_模板.xlsx')
    output = os.path.join(here, '商品总表_模板_填充后.xlsx')

    data = {}
    from erimus.toolbox import *
    for d in MONGODB('easy_market')['goods'].find().sort('row', 1):
        sheet = d['sheet']

        # delete unneeded columns
        for ignore in ['_id', 'update', 'row', 'sheet']:
            d.pop(ignore)

        if '推荐' in d:
            d['推荐'] = 1

        # fill data
        data.setdefault(sheet, [])
        data[sheet].append(d)

    # printFormatJSON(data)

    fill_excel_module(module=module, data=data, output=output)
