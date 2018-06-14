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


def save_wechat_article(item):
    try:
        wechat_article = models.WechatArticle(tittle=item['title'],
                                              author=item['author'].strip(),
                                              summary=item['summary'],
                                              cover=item['cover'],
                                              content=item['content'].strip(),
                                              like_num=item['like_num'],
                                              read_num=item['read_num'],
                                              comment=item['comment'],
                                              url=item['url'],
                                              recieve_time=item['receive_time'],
                                              account=item['account'],
                                              biz=item['biz'])

    except Exception as e:
        print(e)
        return
    wechat_article.save()
    print("成功爬取文字：%" % wechat_article.tittle)
