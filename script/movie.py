#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/21 上午11:47
#   Desc    :   经典电影资源聚集
import requests

from bs4 import BeautifulSoup


# 豆瓣top250电影
URL = 'https://movie.douban.com/top250'

# 阳光电影搜索电影地址
URL1 = 'http://s.dydytt.net/plus/search.php'


def make_result(items, page, size, result_list):
    """ 整理获取到的内容 """
    for num, fi_itmes in enumerate(items):
        num += page*size+1
        movie_info_dict = fi_itmes.find('div', class_='pic').a.img.attrs

        try:
            keyword = movie_info_dict['alt'].encode('gb2312')
        except UnicodeEncodeError:
            movie_info_dict['download_url'] = u'编码问题'
            print u"{num} -- 影片：{name} 海报：{src} 下载地址：{url}".format(
                num=num, name=movie_info_dict['alt'], src=movie_info_dict['src'],
                url=movie_info_dict['download_url'])
            result_list.append(movie_info_dict)
            continue
        args = {'kwtype': 0, 'keyword': keyword}

        # 根据影片名寻找下载地址
        try:
            movie_response = requests.get(URL1, params=args, timeout=8)
        except Exception:
            movie_info_dict['download_url'] = u'查找影片超时'
            print u"{num} -- 影片：{name} 海报：{src} 下载地址：{url}".format(
                num=num, name=movie_info_dict['alt'], src=movie_info_dict['src'],
                url=movie_info_dict['download_url'])
            result_list.append(movie_info_dict)
            continue

        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
        movie_content_soup = movie_soup.find('div', class_='co_content8')
        try:
            movie_detail_url = URL1 + movie_content_soup.td.b.a.attrs['href']
            movie_info_dict['download_url'] = movie_detail_url
            print u"{num} —— 影片：{name} 海报：{src} 下载地址：{url}".format(
                num=num, name=movie_info_dict['alt'], src=movie_info_dict['src'],
                url=movie_info_dict['download_url'])
        except AttributeError:
            movie_info_dict['download_url'] = 'not found'
            print u"{num} -- 影片：{name} 海报：{src} 下载地址：{url}".format(
                num=num, name=movie_info_dict['alt'], src=movie_info_dict['src'],
                url=movie_info_dict['download_url'])
        finally:
            result_list.append(movie_info_dict)


def get_movie(url, args):
    """ 获取豆瓣电影上的TOP250 """
    douban_response = requests.get(url, params=args)
    soup = BeautifulSoup(douban_response.text, 'html.parser')
    items = soup.find_all('div', class_='item')
    return items


def print2markdown(result_list):
    """ 写到md文件中 """
    with open('movie.md', 'wa+') as fb:
        for num, fi_result in enumerate(result_list):
            format_str =u"""第{num}位：{name}  \n![]({src})  \n下载地址：{url}\n\n""".format(
                num=num+1, name=fi_result['alt'], src=fi_result['src'],
                url=fi_result['download_url'])
            fb.write(format_str.encode('utf-8'))


def main(page=0, size=25, count=10):
    result_list = []
    for fi_page in range(1, count+1):
        items = get_movie(URL, {'start': page*size})
        make_result(items, page, size, result_list)
        page = fi_page
    return result_list


# 下载电影地址有问题！
result_list = main()
print2markdown(result_list)
