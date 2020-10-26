# -*- coding: utf-8 -*-
# @Time: 2020/10/10 17:14
# @Author: zrd
# @File: score_service.py
# @Software: PyCharm

from .db_util import *
from .sql_map import sql_movie250


def score_statistic() -> list:
    score_list = select(sql_movie250['score_statistic'])
    score = []
    score_count = []
    for item in score_list:
        score.append(str(item[0]))
        score_count.append(item[1])
    return score, score_count
