# -*- coding: utf-8 -*-
# @Time: 2020/10/10 17:14
# @Author: zrd
# @File: score_service.py
# @Software: PyCharm

from .db_util import *
import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


def get_wordcloud() -> str:
    """
    根据电影简介创建词云图片，返回图片路径
    return : path （图片路径）
    """

    sql = "select intro from movie250"
    data = select(sql)
    intro_str = ' '.join(list(map(lambda x:x[0], data)))

    # 用jieba提取词语
    cut_list = list(jieba.cut(intro_str))
    cut_str = ' '.join(cut_list)

    # 用PIL打开图片，用numpy转换成数组
    # img = Image.open("../static/assets/img/tree.jpg")
    img = Image.open("static/assets/img/tree.jpg")
    img_arr = np.array(img)

    # 用WordCloud创建词云
    wc = WordCloud(
        background_color='white',
        mask=img_arr,  # 图片遮罩，数组形式的图片
        font_path='msyh.ttc'  # 字体所在位置: C:\Windows\Fonts
    )
    wc.generate_from_text(cut_str)

    # 用matplotlib.pyplot绘制图片，并保存
    fig = plt.figure()
    plt.axis('off')
    plt.imshow(wc)
    path = "static/assets/img/word_cloud.jpg"
    plt.savefig(path, dpi=300)
    return path
