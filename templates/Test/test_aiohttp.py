# -*- coding: utf-8 -*-
# @Time: 2020/11/17 13:30
# @Author: zrd
# @File: test_aiohttp.py
# @Software: PyCharm

import asyncio
import aiohttp

urls = ["http://www.baidu.com", "https://www.bilibili.com/","https://movie.douban.com/top250?start="]
htmls = []

async def spiderUrl(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            htmls.append(html)

coroutines = [spiderUrl(url) for url in urls]
coroutine = asyncio.wait(coroutines)
asyncio.run(coroutine)

# tasks = [asyncio.create_task(spiderUrl(url)) for url in urls]
# tasks = asyncio.wait(tasks)
# asyncio.run(tasks)

print(len(htmls))