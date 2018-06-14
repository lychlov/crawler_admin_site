# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     article_crawler
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
import os
import urllib
from urllib.parse import urlparse, parse_qs

import _thread
import pymongo
from time import sleep
import re
import requests
from lxml import etree

from apis.use_api import get_true_video_url, get_article_info
from utils import get_header, get_img_store,save_wechat_article


def url2dict(url):
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])


def set_file_title(title):
    file_name = re.sub('[\/:*?"<>|.]', '', title)  # 去掉非法字符
    return file_name


def check_file_path(dict_info, file_path='', ):
    account = set_file_title(dict_info.get('account', 'unkown'))
    title = set_file_title(dict_info.get('title', 'unkown'))
    file_path = get_img_store()
    file_dir = os.path.join(file_path, account, title)
    if not os.path.exists(file_dir):
        # 如果不存在则创建目录
        #  创建目录操作函数
        os.makedirs(file_dir)
    return file_dir


def download_videos(dict_info, file_path='', video_urls=[]):
    file_dir = check_file_path(dict_info, file_path)
    for fake_url in video_urls:
        headers=get_header()
        vid = url2dict(fake_url).get('vid', 'unknown')
        file_name = vid + ".mp4"
        true_url = get_true_video_url(fake_url)
        video_file = requests.get(true_url, stream=True, timeout=10,headers=headers)
        if video_file.status_code == 403:
            print("下载视频失败")
        with open(file_dir + "/" + file_name, 'wb') as fh:
            for chunk in video_file.iter_content(chunk_size=1024):
                fh.write(chunk)
        print("下载视频：%s 完成" % file_name)
        sleep(10)
    pass


def download_pictures(dict_info, file_path='', picture_urls=[]):
    file_dir = check_file_path(dict_info, file_path)
    for picture_url in picture_urls:
        pic_type = picture_url.split('=')[-1]
        file_name = picture_url.split('/')[4] + "." + pic_type
        try:
            pic = requests.get(picture_url, timeout=5)
            fp = open(file_dir + "/" + file_name, 'wb')
            fp.write(pic.content)  # 写入图片
            fp.close()
        except IOError as e:
            print('文件操作失败', e)
        except Exception as e:
            print('错误 ：', e)
    pass


def crawl_article(dicts):
    """
    :param dicts: 
    """
    for article_dict in dicts:
        sess = requests.Session()
        headers = get_header()
        url = article_dict.get('url')
        print("开始爬取：%s" % url)
        res = sess.get(url, headers=headers)
        selector = etree.HTML(res.text)
        rich_media = selector.xpath(
            "//div[@class='rich_media_inner']/div[@id='page-content']/div[1]/div[2]")[0]
        try:
            author = selector.xpath("//div[@id='meta_content']/span[@class='rich_media_meta rich_media_meta_text']")[
                0].xpath(
                "string(.)")
        except:
            author = ''
        __biz = url2dict(url).get('__biz', '')
        # 正文文字
        content = rich_media.xpath("string(.)")
        # 图片集合
        picture_urls = selector.xpath("//img/@data-src")
        # 视频集合
        video_urls = selector.xpath("//iframe[@class='video_iframe']/@data-src")
        json_info = get_article_info(url)
        if json_info is not None:
            like_num = json_info.get('data', {}).get('zannums', 0)
            read_num = json_info.get('data', {}).get('readnums', 0)

        article_item = {'title': article_dict.get('title', ""), 'author': author,
                        'summary': article_dict.get('summary', ""),
                        'cover': article_dict.get('cover', ""), 'content': content, 'like_num': like_num,
                        'read_num': read_num,
                        'comment': "", 'url': url, 'receive_time': article_dict.get('receive_time', ""),
                        'account': article_dict.get('account', ""), 'biz': __biz}
        try:
            save_wechat_article(article_item)
            print("文章存储完成")
        except Exception as e:
            print(e)
        try:
            download_pictures(dict_info=article_item, picture_urls=picture_urls)
            _thread.start_new_thread(download_videos,(article_item, '', video_urls))
        except:
            print("下载多媒体内容失败")
        sleep(60)
    pass
