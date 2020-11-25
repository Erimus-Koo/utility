#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
使用win32控制excel，主要用来给模板文件添加数据。
pip install pywin32
'''
from win32com.client import Dispatch

# ═══════════════════════════════════════════════


class WriteExcel():
    def __init__(self, file):
        self.file = file.encode('gbk')  # 中文需要转码
        self.app = Dispatch('Excel.Application')
        self.wb = self.app.Workbooks.Open(self.file)
        self.app.Calculation = False  # 关闭自动计算
        self.app.DisplayAlerts = False  # 禁止提示警告
        self.app.ScreenUpdating = False  # 禁止屏幕刷新
        self.app.EnableEvents = False  # 禁止提示警告

    def insert(self, *, sheet=1, row=None, column=None):
        # 默认在当前行/列前插入
        # 可以是行列编号(1开始) 插入单行 或者 "2:5"这样插入多行
        if row is not None:
            self.wb.Worksheets(sheet).Rows(row).Insert()
        if column is not None:
            self.wb.Worksheets(sheet).Columns(column).Insert()

    def delete(self, *, sheet=1, row=None, column=None):
        # 可以是行列编号(1开始) 插入单行 或者 "2:5"这样插入多行
        if row is not None:
            self.wb.Worksheets(sheet).Rows(row).Delete()
        if column is not None:
            self.wb.Worksheets(sheet).Columns(column).Delete()

    def copy_sheet(self, src, new=None):
        print(f'Copy sheet: {src} -> {new or src}')
        sht = self.wb.Worksheets(src)
        sht.Copy(sht)  # 复制的表在原表左侧
        if new:  # 新表命名
            self.wb.Activesheet.Name = new

    def delete_sheet(self, sheet):
        print(f'Delete sheet: {sheet}')
        self.wb.Worksheets(sheet).Delete()

    def set_value(self, *, sheet=1, row, column, value):
        self.wb.Worksheets(sheet).Rows(row).Columns(column).Value = value

    def save_and_close(self, save_as=None):
        self.app.Calculation = True  # 重新启用自动计算
        self.app.DisplayAlerts = True  # 禁止提示警告
        self.app.ScreenUpdating = True  # 禁止屏幕刷新
        self.app.EnableEvents = True  # 禁止提示警告
        self.wb.Application.CalculateFullRebuild()  # 自动计算一遍
        if save_as:
            # 即便用了另存 之前的操作也是在原始表上进行的 所以还是建议先复制
            print(f'Save as: {save_as}')
            self.wb.SaveAs(save_as)
        else:
            print(f'Save: {self.file.decode("gbk")}')
            self.wb.Save()
        self.wb.Close(SaveChanges=0)


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    import os
    here = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(here, '商品总表_模板.xlsx')
    output = os.path.join(here, '商品总表_模板_修改后.xlsx')
    os.system(f'copy "{module}" "{output}"')

    excel = WriteExcel(output)
    excel.copy_sheet(src='module', new='new')
    excel.delete_sheet('module')
    excel.insert(row=2)
    excel.insert(column=2)
    excel.delete(row=5)
    excel.delete(column='B:C')
    excel.save_and_close()
