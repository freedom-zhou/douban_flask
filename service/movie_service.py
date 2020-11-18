# -*- coding: utf-8 -*-
# @Time: 2020/9/17 10:49
# @Author: zrd
# @File: movie_service.py.py
# @Software: PyCharm

from .db_util import *
from .sql_map import sql_movie250


def select_all() -> list:
    movie_list = select(sql_movie250['select_all'])
    return movie_list

def select_page(page) -> list:
    num = 10
    st = num * (page-1) + 1
    ed = st + num - 1
    movie_list = select(sql_movie250['select_page'].format(st, ed))
    return movie_list

def get_pages(cur_page, n=5, max=25) -> tuple:
    st = int(cur_page - (n-1)/2)
    ed = st + n
    if st < 1:
        st, ed = 1, n+1
    if ed > max:
        st, ed = max-n, max+1
    return tuple(range(st, ed))