#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 商品凑单算法
# 计算有限个商品，达到指定价格的所有排列组合。

import logging as log

# ═══════════════════════════════════════════════


class Order():

    def __init__(self, itemList, targetPrice):
        self.r = {}
        self.itemList = itemList  # 商品字典{price:nume}
        self.targetPrice = targetPrice  # 凑单目标价格

    def orderNum(self, itemList, prevOrder='', prevPrice=0):
        log.debug(f'>> prevOrder: {prevOrder} | prevPrice: {prevPrice}')
        for num in range(999):
            price, name = itemList[0]
            thisOrder = prevOrder + (f' + {num} {name}' if num else '')
            thisPrice = prevPrice + price * num
            log.debug(f'{thisOrder} = {prevPrice} + {price} * {num}')

            # 如果当前价格超了 就不再增加数量
            if thisPrice >= self.targetPrice:
                self.r[thisOrder.strip('+ ')] = thisPrice
                [log.debug(f'>>> {k} = {v}') for k,v in self.r.items()]
                return

            # 如果价格没超 就往下一位
            if len(itemList) > 1:
                self.orderNum(itemList[1:], prevOrder=thisOrder, prevPrice=thisPrice)

    def calc(self):
        # 格式化商品数据
        itemDict = {}
        for name, price in self.itemList.items():
            itemDict.setdefault(price, '')
            itemDict[price] += f'/{name}'
            itemDict[price] = itemDict[price].lstrip('/')
        itemList = sorted(itemDict.items(), key=lambda x: x[1])
        print('\nITEMLIST\n========')
        [print(f'{price:8.2f} | {name}') for price, name in itemList]
        print(f'\nTraget Price: {targetPrice:.2f}')

        self.orderNum(itemList)
        # 按总价升序
        r = sorted(self.r.items(), key=lambda d: d[1])
        print('\nRESULT\n======')
        [print(f'{total:>8.2f} | {order}') for order, total in r]


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    # log.basicConfig(level=log.DEBUG, format=('pid:%(process)d | %(message)s'))

    itemList = {'鸡胸': 29.8, '鸡腿': 18.8, '麦片': 24.8}
    targetPrice = 198  # 目标价格（满减/包邮/等）

    minOrder = Order(itemList, targetPrice)
    minOrder.calc()
