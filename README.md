# 微信公众号监控及文章爬取
## 需求
1. 实时监控目标微信号发文情况
2. 爬取微信文章中的文字内容存入入库，爬取图片、视频存储入库。
## 主要功能模块
1. 微信监控模块：实现微信的模拟登陆，监视目标公众号发文情况。
2. 文章爬取模块：在微信监控模块获取文章后启动，对文章文字、图片、视频等下载保存。
3. api调用模块：
    - 视频真实地址获取API
    - 文章阅读点赞获取API
## 安装与运行
### 环境要求
- Python3.4
- Mongodb
- 网络环境稳定
- 长期在线的微信（手机或模拟器中）
### 安装
下载软件包
``` shell
cd MPWatcher
pip3 install -r requirements.txt
```
### 配置文件
``` yaml
//目标公众号名称列表
TARGET_MP:
    - MP: "人民网"
    - MP: "新华社"
    - MP: "泰国星暹日报"
    - MP: "泰国世界日报"
    - MP: "泰国网"
    - MP: "Lychlov"
//图片、视频存储路径
IMG_STORE: "/home/docker/work_space/IMG_STORE"

MYSQL_CONNECT: ''
//MongoDB连接字符串
MONGO_URI: 'mongodb://czk:czk10101@127.0.0.1/test'
//真实视频地址API
TRUE_VIDEO_API_URL: 'http://v.ranks.xin/video-parse.php?url='
//阅读点赞API
ARTICLE_INFO_API_URL: 'http://wxapi.51tools.info/wx/api.ashx?key=ps_499658904&ver=1'
```
### 运行
1. 执行命令
``` shell
python3 wechat/watcher.py
```
2. 使用手机或模拟器扫码登陆微信
## 数据结构
----
### 文章表 ###
> 表名`wechat_article`

| 字段名              | 数据类型| 长度 | 说明       | 描述 |
|:-------------------|:-------|:-----|:--------- |:----|
|_id|number|||文章id|
|title|varchat|||标题|
|author|varchat|||作者|
|summary|varchat|||文章简介|
|cover|varchat|||简介处贴图|
|content|clob|||内容|
|like_num|number|||点赞数|
|read_num|number|||阅读数|
|comment|json|||评论信息|
|url|varchat|||文章链接|
|recieve_time|date|||发布时间|
|account|varchat|||公众号名|
|__biz|varchat|||公众号唯一参数 可关联公众号表|

