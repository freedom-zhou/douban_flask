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
