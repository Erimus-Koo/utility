#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# excel入库通用程序，包括log历史版本。

from .read import read_excel
from util.mongo.save_data_to_db import save_data_to_db

# ═══════════════════════════════════════════════


def excel_to_mongodb(*,
                     excel_file,        # 数据来源
                     header=0,          # excel 标题行前空几行
                     sheet=None,        # 表名称 数组 None为全部
                     df_format=None,    # excel 各列格式化 跟type_dict功能接近
                     db,                # 数据库
                     collection,        # 集合名称（备份会自动加history）
                     main_key='id',     # 数据库的主键
                     type_dict={},      # 指定各列的数据类型 {列名:类型}
                     format_data=None,  # 自定义格式化数据的函数
                     ):
    # read excel content
    excel = read_excel(excel_file, sheet=sheet, header=header, df_format=df_format)

    # read old data in database
    old_data = {}
    for d in db[collection].find():
        old_data[d[main_key]] = d

    # update data
    result = {}
    for sheet_name, data in excel.items():
        for i, row in enumerate(data):
            # format data type
            for k, v in row.items():
                if k not in type_dict:
                    continue

                fmt = type_dict[k]  # 目标格式

                if fmt == 'ignore' and k in row:  # 移除要忽略的列
                    row.pop(k)
                    continue

                # 避免int读取为float 如123会读取为123.0 转string时会出错
                if fmt==str and isinstance(v, float) and int(v) == v:
                    v = int(v)

                if not isinstance(v, fmt):  # 格式化为目标数据类型
                    try:  # 比如空内容转int会出错
                        row[k] = fmt(v)
                    except:
                        pass

                if fmt == str:  # 替换单元格内的换行符 移除前后空格
                    row[k] = row[k].strip()

            # custom format data rules
            if format_data:
                row = format_data(row)

            # 删除空数据
            # 如果放在前面 format_data就需要不停判断字段是否存在 所以放到这里
            [row.pop(k) for k, v in row.copy().items() if not v]

            # 记录原表的信息 将来需要重新写回excel时会用到
            row['sheet'] = sheet_name  # 表名
            row['row'] = i + 1  # 在原表的行数 将来可用来排序
            # print(f'row_{i+1}: {row}')

            # data -> mongodb
            old_row = old_data.get(row[main_key], {})
            r = save_data_to_db(db, collection,
                                new=row, old=old_row,
                                match_key=[main_key])
            if r['info'] != 'same':  # 打印有变化的数据
                print(r['info'], r['data'])

            # 统计结果
            result.setdefault(r['info'], 0)
            result[r['info']] += 1

    print('---\nExcel to mongodb result:')
    [print(f'{k}: {v}') for k, v in result.items()]


# Example
def format_data(row):
    # 特殊处理 data should be int, but excel auto read as float, remove ".0".
    if row.get('条码', '').endswith('.0'):
        row['条码'] = row['条码'][:-2]

    return row


# ═══════════════════════════════════════════════
# 各字段数据类型
type_dict = {
    'id': str,
    '货源': str,
    '条码': str,
    '品类': str,
    '子类': str,
    '品牌': str,
    '淘宝id': int,
    '链接': 'ignore',  # 无需采集
    '品名': str,
    '别名': str,
    '描述': str,
    '备注': str,
    '推荐': bool,
    '下架': bool,
    '指导价': float,
    '淘宝价': float,
    '限价': float,
    '拿货价': float,
    '代发价': float,
}
# ═══════════════════════════════════════════════

if __name__ == '__main__':

    excel_to_mongodb(excel_file=LATEST_COST,
                     db=DB,
                     collection=COLLECTION,
                     main_key=MAIN_KEY,
                     type_dict=type_dict,
                     format_data=format_data
                     )
