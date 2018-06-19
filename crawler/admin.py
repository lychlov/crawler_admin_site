from django.contrib import admin
from .models import TargetMP, WechatArticle, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    exclude = ('logo_url','nick_name','content','create_time','like_num')
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    list_display=('detail',)


# Register your models here.
class WechatArticleAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'account', 'summary', 'recieve_time')
    list_filter = ['recieve_time', 'account']
    search_fields = ['content']
    inlines = [CommentInline]


admin.site.register(TargetMP)
admin.site.register(WechatArticle, WechatArticleAdmin)
admin.site.register(Comment,CommentAdmin)
