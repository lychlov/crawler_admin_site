# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MPS
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
import time

import django
import sys

import os

sys.path.insert(0, 'D:/PycharmProjects/crawler_admin_site/')
os.environ["DJANGO_SETTINGS_MODULE"] = "crawler_admin_site.settings"
django.setup()

from crawler import models

set_inf = models.TargetMP.objects.all()
MP_ACCOUNT = []
for info in set_inf:
    MP_ACCOUNT.append(info.name)


def save_wechat_article(item, comment_info_json):
    try:
        wechat_article = models.WechatArticle(tittle=item['title'],
                                              author=item['author'].strip(),
                                              summary=item['summary'],
                                              cover=item['cover'],
                                              content=item['content'].strip(),
                                              like_num=item['like_num'],
                                              read_num=item['read_num'],
                                              url=item['url'],
                                              recieve_time=item['receive_time'],
                                              account=item['account'],
                                              biz=item['biz'],
                                              pictures=str(item['pictures']),
                                              )
        wechat_article.save()
        logo_url_list = []
        if comment_info_json.get('count', 0) > 0:
            comment_data = comment_info_json.get('data', [])
            for comment in comment_data:
                c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.get('create_time', '')))
                wechat_article.comment_set.create(nick_name=comment.get('nick_name', ''),
                                                  logo_url=comment.get('logo_url', ''),
                                                  content=comment.get('content', ''),
                                                  create_time=c_time,
                                                  like_num=comment.get('like_num', ''))
                logo_url_list.append(comment.get('logo_url', ''))
    except Exception as e:
        print(e)
    print("成功爬取文章：%" % wechat_article.tittle)
