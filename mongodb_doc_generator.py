#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 用来检查各个collection的字段，排查类型和编写文档。

import os
import yaml

# ═══════════════════════════════════════════════


def mongodb_doc_generator(*, DB, collection_name, doc_path):
    '''
    DB: mongodb的指定DB实例 pymongo.MongoClient()[dbname]
    collecton_name: str
    doc_path: 生成的文档所在的目录

    读取mongodb，汇总所有出现过的key，统计去重后数值数量、类型、出现次数，并附上5个sample。
    适用于爬虫等数据的统计、分析、清洗准备、等。

    可以在doc目录下写一个{collection_name}.yaml文件，给已知字段加入备注。

    最终生成的{collection_name}.md中的字段排序以yaml为准。yaml中没有的升序排列。
    '''

    # count key and value types in collection
    r = {}  # collect all keys and its infos
    total = DB[collection_name].count_documents({})
    for d in DB[collection_name].find():
        d.pop('_id')
        for k in d:
            r.setdefault(k, {'count': 0, 'type': [], 'exist': 0, 'sample': []})
            r[k]['exist'] += 1
            if d[k] not in r[k]['sample']:
                r[k]['count'] += 1
                if len(r[k]['sample']) < 5:  # limit set scale
                    r[k]['sample'].append(d[k])

            _type = type(d[k]).__name__
            if _type not in r[k]['type']:
                r[k]['type'].append(_type)

    # read description
    desc_yaml = os.path.join(doc_path, f'{collection_name}.yaml')
    if os.path.exists(desc_yaml):
        with open(desc_yaml, 'r', encoding='utf-8') as f:
            desc = yaml.safe_load(f)
    else:
        desc = {}

    # 优先按照desc里的顺序排序 其余的按key升序
    ordered_r = []
    for k, v in desc.items():
        if k in r:
            ordered_r.append((k, r.pop(k)))
    ordered_r += sorted(r.items(), key=lambda x: x[0])
    unknown_keys = r.keys()  # keys not in yaml

    # print result in markdown
    print('=' * 80)
    md = []
    # title
    md.append(f'# [{collection_name}] 字段说明\n')
    # table
    md.append('key | value\n--- | ---')
    for k, v in ordered_r:
        md.append(f'{k} | {desc.get(k, "?")}')
    # key details
    for k, v in ordered_r:
        md.append(f'\n## {k}  \n**desc** {desc.get(k, "?")}  \n'
                  f'**type** `{", ".join(v["type"])}` | '
                  f'**count** `{v["count"]}` | '
                  f'**exist** `{v["exist"]}` | '
                  f'**not exist** `{total-v["exist"]}`')
        md.append('```')  # sample data
        [md.append(f'{sample.__repr__()}') for sample in v["sample"]]
        md.append('```')

    md_text = '\n'.join(md)
    print(md_text)
    output = os.path.join(doc_path, f'{collection_name}.md')
    with open(output, 'w', encoding='utf-8') as f:
        f.write(md_text)

    if unknown_keys:
        print(f'{"="*50}\nBelow keys not in Yaml')
        [print(k) for k in unknown_keys]


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    import pymongo
    DB = pymongo.MongoClient(host=['127.0.0.1:27017'])['test']
    collection_name = 'test'
    doc_path = os.path.abspath(os.path.dirname(__file__))

    mongodb_doc_generator(DB=DB,
                          collection_name=collection_name,
                          doc_path=doc_path)
