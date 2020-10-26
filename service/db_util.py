# -*- coding: utf-8 -*-
# @Time: 2020/9/17 12:21
# @Author: zrd
# @File: db_util.py
# @Software: PyCharm

import sqlite3

db_path = r'data/db/movie.db'

def select(sql) -> list:
    result_list = []
    # 创建连接和游标
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 获取数据并保存
    result = cursor.execute(sql)
    for e in result:
        result_list.append(e)
    # 关闭游标和连接
    cursor.close()
    conn.close()
    # 返回查询结果
    return result_list
