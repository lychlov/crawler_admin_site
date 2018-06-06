# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     use_api.py
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
import json

import requests

from utils import get_header, get_true_video_api_url, get_article_info_api_url

TRUE_VIDEO_API_URL = get_true_video_api_url()
ARTICLE_INFO_API_URL = get_article_info_api_url()


def get_true_video_url(fake_url):
    sess = requests.Session()
    headers = get_header()
    url = TRUE_VIDEO_API_URL + fake_url
    try:
        res = sess.get(url, headers=headers)
        result = json.loads(res.text, encoding='utf-8')
        string = result.get('data')[0].get('url')
        return string
    except Exception as e:
        print("视频真实地址API调用失败")
        print(e)


def get_article_info(article_url):
    headers = get_header()
    url = ARTICLE_INFO_API_URL
    data = {'url': article_url}
    try:
        res = requests.post(url, headers=headers, data=data)
        json_info = json.loads(res.text, encoding='utf-8')
        if json_info.get('msg', '') == 'succ':
            return json_info
        else:
            print("接口调用失败原因 %s" % json_info.get('msg', ''))
            return None

    except Exception as e:
        print("阅读点赞API调用失败")
        print(e)
