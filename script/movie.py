#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/21 上午11:47
#   Desc    :   经典电影资源聚集
import re

import requests

from bs4 import BeautifulSoup


# 豆瓣top250电影
URL = 'https://movie.douban.com/top250'

# 阳光电影搜索电影地址
URL1 = 'http://s.dydytt.net/plus/search.php'


douban_response = requests.get(URL)
soup = BeautifulSoup(douban_response.text, 'html.parser')
items = soup.find_all("div", class_="item")


for i, fi_itmes in enumerate(items):
    img_dic = fi_itmes.find("div", class_="pic").a.img.attrs
    args = {'kwtype': 0, 'keyword': img_dic['alt'].encode('gb2312')}
    movie_response = requests.get(URL1, params=args)
    movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
    movie_content_soup = movie_soup.find('div', class_='co_content8')
    try:
        movie_detail_url = URL1 + movie_content_soup.td.b.a.attrs['href']
        movie_detail_content = requests.get(movie_detail_url).text
        print movie_detail_content
        movie_detail_soup = BeautifulSoup(movie_detail_content, 'html.parser')
        print movie_detail_soup.find('div')
            # (thunderrestitle=re.compile("ftp://[^\s?]*"))
    except AttributeError:
        print 'not found'
    print u"{i} —— 影片：{alt} 海报：{src} ".format(i=i, alt=img_dic['alt'], src=img_dic['src'])
