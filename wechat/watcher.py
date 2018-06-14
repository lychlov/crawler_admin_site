# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wechat_watcher
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
from wxpy import *
import re
import sys
sys.path.append("D:/PycharmProjects/crawler_admin_site")
from utils import MP_ACCOUNT
from wechat_crawler import crawl_article


logger = logging.getLogger(__name__)

# bot = Bot(, console_qr=1,qr_path='')
bot = Bot(cache_path=True)



# bot.self.send('能收到吗？')


# bot.add_mp(user='oNetwork')

def check_mps():
    my_mps = bot.mps(update=True)


@bot.register(msg_types=SHARING, except_self=False)
def auto_add_mps(msg):
    if msg.sender.name in MP_ACCOUNT or msg.sender.name is bot.self.name:
        print("hit %s" % msg.sender.name)
    else:
        print("miss %s" % msg.sender.name)
        return
    article_dicts = []
    if msg.articles is None:
        msg_dict = dict()
        msg_dict['url'] = msg.url
        msg_dict['title'] = msg.file_name
        xml_str = msg.raw['Content']
        summary = ""
        try:
            summary = re.findall(r"<des>(.+)?</des>", xml_str).pop()
        except:
            pass
        cover = re.findall(r"<thumburl>(.+?)</thumburl>", xml_str).pop()
        try:
            account = re.findall(r"<sourcedisplayname>(.+?)</sourcedisplayname>", xml_str).pop()
        except:
            account = ''
        msg_dict['summary'] = summary
        msg_dict['cover'] = cover
        msg_dict['receive_time'] = msg.receive_time
        msg_dict['account'] = account
        alert_msg = "接收到推文来自：%s\n标题：%s\n url:%s" % (account, msg.file_name, msg.url)
        bot.file_helper.send(alert_msg)
        article_dicts.append(msg_dict)
        # return
    else:
        for article in msg.articles:
            temp_dict = dict()
            temp_dict['url'] = article.url
            temp_dict['title'] = article.title
            temp_dict['summary'] = article.summary
            temp_dict['cover'] = article.cover
            temp_dict['receive_time'] = msg.receive_time
            temp_dict['account'] = msg.sender.name
            alert_msg = "接收到推文来自：%s\n标题：%s\n url:%s" % (msg.sender.name, article.title, article.url)
            # 通知用户接受文章
            article_dicts.append(temp_dict)
            bot.file_helper.send(alert_msg)
    crawl_article(article_dicts)


# temp_dict = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
#              "summary": 'jianjie',
#              "cover": "http://sdfsdf",
#              "receive_time": "2018-05-23 23:23:23",
#              "account": '泰国网'}
# crawl_article(url=url, dict_info=temp_dict)

embed()
