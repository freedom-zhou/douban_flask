# -*- coding: utf-8 -*-
# @Time: 2020/8/29 17:59
# @Author: zrd
# @File: douban.py
# @Software: PyCharm

from typing import List
from functools import wraps
import time
import os

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 定制url，获取网页数据
import xlwt  # 对excel2003格式文件xls进行写操作
import xlsxwriter as xxwt  # 对excel2007格式文件xlsx进行写操作
import sqlite3  # 进行数据库操作
import asyncio  # 协程实现异步io
import aiohttp  # 异步爬取数据
from multiprocessing import Pool as ProcessPool # 实现多进程
from multiprocessing.dummy import Pool as ThreadPool # 实现多线程

def main():
    baseUrl = 'https://movie.douban.com/top250?start='
    # savepath = r'./data/excel/豆瓣电影top250.xls'
    # savepath = r'./data/excel/豆瓣电影top250.xlsx''
    dbpath = r'./data/db/movie.db'

    # 爬取网页并解析数据
    # 同步方式爬取数据
    # datalist = getData(baseUrl)
    # 协程 异步方式爬取数据
    datalist = getDataAsync1(baseUrl)
    # 多线程 异步方式爬取数据
    # datalist = getDataAsync2(baseUrl)
    # 多进程 异步方式爬取数据
    # datalist = getDataAsync3(baseUrl)

    # 保存数据
    # saveData2excel(savepath, datalist)
    # saveData2db(dbpath, datalist)

    # print("\n", "-"*50, "\n", datalist)


# 影片详情链接
patt_a = re.compile(r'<a href="(.*)">')
# 影片图片
patt_img = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 包括换行符、
# 影片片名
patt_name = re.compile(r'<span class="title">(.*?)</span>')
# 影片评分
patt_rate = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评价人数
patt_judge = re.compile(r'<span>(\d*)人评价</span>')
# 概述
patt_intr = re.compile(r'<span class="inq">(.*?)</span>')
# 相关内容
patt_about = re.compile(r'<p class="">(.*?)</p>', re.S)

def showRunTime(f):
    @wraps(f)
    def func(*args, **kwargs):
        st = time.time()
        res = f(*args, **kwargs)
        ed = time.time()

        print(f"{f.__doc__} 耗时 {ed-st} 秒 len(result)={len(res)}")
        return res
    return func

def askUrl(url: str) -> str:
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    html = ''
    req = urllib.request.Request(url, headers=head)

    try:
        print(f'开始爬取数据 url: {url}')
        response = urllib.request.urlopen(req, timeout=3)
        html = response.read().decode('utf-8')
        print(f'爬取数据成功 url: {url}')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

    return html

async def askUrlAsync(url: str, datalist: List[List]) -> str:
    async with aiohttp.ClientSession() as session:
        print(f'开始爬取数据 url: {url}')
        async with session.get(url) as response:
            print(f'爬取数据成功 url: {url}')
            html = await response.text()
            datas = parseData(html)
            datalist.extend(datas)

@showRunTime
def getData(baseurl: str) -> List[List]:
    """同步方式爬取数据"""
    datalist = []

    urls = [baseurl + str(i * 25) for i in range(10)]
    for url in urls:
        html = askUrl(url)
        datas = parseData(html)
        datalist.extend(datas)

    return datalist

@showRunTime
def getDataAsync1(baseurl: str) -> List[List]:
    """协程 异步方式爬取数据"""
    datalist = []
    urls = [baseurl + str(i * 25) for i in range(10)]

    coroutines = [askUrlAsync(url, datalist) for url in urls]
    coroutine = asyncio.wait(coroutines)
    asyncio.run(coroutine)

    return datalist

@showRunTime
def getDataAsync2(baseurl: str) -> List[List]:
    """多线程 异步方式爬取数据"""
    datalist = []
    urls = [baseurl + str(i * 25) for i in range(10)]
    with ThreadPool() as pool:
        htmls = pool.map(askUrl, urls)
    for html in htmls:
        datalist.extend(parseData(html))
    return datalist

@showRunTime
def getDataAsync3(baseurl: str, process_num=os.cpu_count()) -> List[List]:
    """多进程 异步方式爬取数据"""
    datalist = []
    urls = [baseurl + str(i * 25) for i in range(10)]
    with ProcessPool(process_num) as pool:
        htmls = pool.map(askUrl, urls)
    for html in htmls:
        datalist.extend(parseData(html))
    return datalist

def parseData(html) -> List[List]:
    soup = BeautifulSoup(html, 'lxml')
    datalist = []
    for item in soup.find_all('div', class_='item'):
        data = []
        item = str(item)
        # 影片详情链接
        li = patt_a.findall(item)[0]
        data.append(li)
        # 影片图片
        li = patt_img.findall(item)[0]
        data.append(li)
        # 影片片名 中文
        lis = patt_name.findall(item)
        data.append(lis[0])
        # 影片片名 外文
        if len(lis) == 2:
            data.append(lis[1].replace('/', '').strip())
        else:
            data.append(' ')
        # 影片评分
        li = patt_rate.findall(item)[0]
        data.append(li)
        # 评价人数
        li = patt_judge.findall(item)[0]
        data.append(li)
        # 概述
        li = patt_intr.findall(item)
        if len(li) > 0:
            li = li[0].replace('。', '')
            data.append(li)
        else:
            data.append(' ')
        # 相关内容
        li = patt_about.findall(item, re.S)[0]
        li.replace('/', ' ')
        li = re.sub(r'<br\s*/\s*>', ' ', li)
        mt = re.search(r'(导演.*)\n.*(\d{4}).* / (\D*?) / (.*)$', li.strip())
        if mt is None:
            print(li.strip(), '\n')
        actor, year, country, keys = mt.groups()
        # 导演、演员
        data.append(actor.strip())
        # 年份
        data.append(year.strip())
        # 国家
        data.append(country.strip())
        # 关键词
        data.append(keys.strip())

        datalist.append(data)
    return datalist

def saveData2excel(savepath: str, datalist: List[List]) -> None:
    if not isinstance(savepath, str):
        return
    elif savepath.endswith('xls'):
        print(f'保存中...')
        book = xlwt.Workbook('utf-8')
        sheet = book.add_sheet('豆瓣top250', cell_overwrite_ok=True)

        head = ['影片详情链接', '影片图片链接', '中文名', '外文名', '评分', '人数', '概述', '导演/演员', '年份', '国家', '关键词']
        # 填表头
        print(f'写入表头...')
        for i, v in enumerate(head):
            sheet.write(0, i, v)
        # 填内容
        for i, item in enumerate(datalist):
            print(f'写入第{i+1}条...')
            for j, e in enumerate(item):
                sheet.write(i+1, j, e)
        # 保存
        book.save(savepath)

    elif savepath.endswith('xlsx'):
        print(f'保存中...')
        book = xxwt.Workbook(savepath)
        sheet = book.add_worksheet('豆瓣top250')

        head = ['影片详情链接', '影片图片链接', '中文名', '外文名', '评分', '人数', '概述', '导演/演员', '年份', '国家', '关键词']
        # 填表头
        print(f'写入表头...')
        sheet.write_row('A1', head)

        # 填内容
        for i, item in enumerate(datalist):
            print(f'写入第{i+1}条...')
            sheet.write_row('A'+str(i+2), item)

        book.close()

def saveData2db(dbpath: str, datalist: List[List]) -> None:
    if not isinstance(dbpath, str):
        return
    else:
        init_db(dbpath)

        print(f'保存中...')
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        for ind, datas in enumerate(datalist):
            for i in range(len(datas)):
                datas[i] = '"' + datas[i] + '"'
            sql = '''
                insert into movie250(info_link, img_link, c_name, e_name, score, p_num, intro, actor, year, country, keys) 
                values ({})
            '''.format(','.join(datas))
            try:
                print(f'保存第{ind+1}条数据到数据库...')
                cursor.execute(sql)
            except sqlite3.OperationalError as e:
                print(e)
                print('sql: ', sql)
                print('datas: ', datas)
                conn.close()
                return

        conn.commit()
        print('数据保存成功！')
        conn.close()

def init_db(path: str):
    conn = sqlite3.connect(path)
    sql = '''
        create table if not exists movie250(
            id integer not null primary key autoincrement,
            info_link text not null,
            img_link text not null,
            c_name varchar(50) not null,
            e_name varchar(50),
            score real not null,
            p_num int not null,
            intro text,
            actor text,
            year int,
            country text,
            keys text
        )
    '''
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':  # 程序执行时
    main()
