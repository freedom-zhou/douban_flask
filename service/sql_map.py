# -*- coding: utf-8 -*-
# @Time: 2020/9/17 12:10
# @Author: zrd
# @File: sql_map.py
# @Software: PyCharm

sql_movie250 = {
    "select_all":
        '''select id,
               info_link,
               img_link,
               c_name,
               e_name,
               score,
               p_num,
               intro,
               actor,
               year,
               country,
               keys
        from movie250''',

    "select_page":
        '''select id,
               info_link,
               img_link,
               c_name,
               e_name,
               score,
               p_num,
               intro,
               actor,
               year,
               country,
               keys
        from movie250
        where id between {} and {}
        ''',

    "count_all":
        '''select count(*)
        from movie250
        ''',

    "score_statistic":
        "select score, count(score) from movie250 group by score"
}
