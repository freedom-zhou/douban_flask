# -*- coding: utf-8 -*-
# @Time: 2020/10/12 13:31
# @Author: zrd
# @File: testWordCloud.py
# @Software: PyCharm

import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import sqlite3

# 从数据库读取电影简介
db_path = r'../../data/db/movie.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sql = "select intro from movie250"
data = cursor.execute(sql)
intro_str = ' '.join(list(map(lambda x:x[0],data)))

cursor.close()
conn.close()

# print(intro_str)

# 用jieba提取词语
cut_list = list(jieba.cut(intro_str))
cut_str = ' '.join(cut_list)
# print(len(cut_list))
# print(cut_str)

# 用PIL打开图片，用numpy转换成数组
img = Image.open("./img/tree.jpg")
img_arr = np.array(img)

# 用WordCloud创建词云
wc = WordCloud(
    background_color='white',
    mask=img_arr,   # 图片遮罩，数组形式的图片
    font_path='msyh.ttc' # 字体所在位置: C:\Windows\Fonts
)
wc.generate_from_text(cut_str)

# 用matplotlib.pyplot绘制图片，并保存
fig = plt.figure()
plt.axis('off')
plt.imshow(wc)
plt.savefig("./img/word_cloud.jpg", dpi=350)