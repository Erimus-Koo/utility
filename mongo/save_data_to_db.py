#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# # 比较差异后 分别写入变化字段和最终字段
# # 例如，最终记录数据的数据库为user，记录变更历史的就是user_history。
# # 最终库为了查询结果快速，历史库是为了节省空间。
# # match_key是该记录在库中的唯一条件，可以为组合key。
# # 比如某条微博下某人的点赞，bid+uid，点赞本身的id也许没有或不可知。

import pymongo
import time

# ═══════════════════════════════════════════════


def save_data_to_db(
    db,                     # 库
    collection,             # 集合名
    *,
    old=None,               # 旧数据
    new,                    # 要存入的新数据
    match_key=('id'),       # 跟旧数据比对查询用的主键 可多个
    log_update_time=False   # 强制更新update时间
):
    '''
    带历史记录的数据库写入

    collection_history 库，仅写入这次变化的部分（包含主键）。
    collection 写入完整的数据。注：新数据如果减少了字段，并不会被删除。

    在有些爬虫里，如果数据未更新，则无法判断最近一次采集的时间。
    所以有时候会根据需要，每次强制去collection更新一下update的时间戳作为标记。
    '''

    # 组装查询条件
    cdt = {}
    for k in match_key:
        cdt[k] = new[k]

    # 没有旧数据的话 查询旧数据
    if old is None:
        old = db[collection].find_one(cdt) or {}

    # 过滤出新增或变化数据
    diff = cdt.copy()  # 录入history时需含有主键

    changed = False  # 标记是否有变化
    for key, new_value in new.items():
        if new_value != old.get(key):
            diff[key] = new_value  # 记录变化字段
            changed = True

    if changed:  # 有字段新增或变化
        # 更新 历史库记录增变部分
        db[collection + '_history'].insert_one(diff.copy())
        status = 'changed' if old else 'new'
    else:
        status = 'same'

    if changed or log_update_time:
        # 更新 结果数据库
        diff['update'] = int(time.time())  # 写入更新时间
        db[collection].update_one(cdt, {'$set': diff}, upsert=True)

    return {'info': status, 'data': diff}


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    # 常用方式
    save_data_to_db(DB, COLLECTION, old=old, new=new, match_key=('uid'))
