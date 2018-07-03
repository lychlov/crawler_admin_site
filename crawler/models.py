from django.db import models


# Create your models here.
# |title|varchat|||标题|
# |author|varchat|||作者|
# |summary|varchat|||文章简介|
# |cover|varchat|||简介处贴图|
# |content|clob|||内容|
# |like_num|number|||点赞数|
# |read_num|number|||阅读数|
# |comment|json|||评论信息|
# |url|varchat|||文章链接|
# |recieve_time|date|||发布时间|
# |account|varchat|||公众号名|
# |__biz|varchat|||公众号唯一参数 可关联公众号表|

class WechatArticle(models.Model):
    tittle = models.CharField('标题', max_length=100)
    author = models.CharField('作者', max_length=20,blank=True)
    summary = models.CharField('摘要', max_length=300)
    cover = models.CharField('封面图链接', max_length=300)
    content = models.TextField('文章内容')
    like_num = models.IntegerField('点赞', default=0)
    read_num = models.IntegerField('阅读', default=0)
    url = models.URLField('文章链接',max_length=500)
    recieve_time = models.DateTimeField('发布时间')
    account = models.CharField('公众号', max_length=20)
    biz = models.CharField(max_length=50)

    def __str__(self):
        return self.tittle


class Comment(models.Model):
    nick_name = models.CharField('昵称', max_length=100)
    logo_url = models.URLField('头像链接地址')
    content = models.TextField('评论内容')
    create_time = models.DateTimeField('评论时间')
    like_num = models.IntegerField('点赞', default=0)
    wechat_article = models.ForeignKey(WechatArticle, on_delete=models.CASCADE)

    def __str__(self):
        return "%s ： %s \n点赞：%s" % (self.nick_name, self.content, self.like_num)

    def detail(self):
        return "%s ： %s \n点赞：%s" % (self.nick_name, self.content, self.like_num)


class TargetMP(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
