from django.contrib import admin
from .models import TargetMP, WechatArticle, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


# Register your models here.
class WechatArticleAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'account', 'summary', 'recieve_time')
    list_filter = ['recieve_time', 'account']
    search_fields = ['content']
    inlines = [CommentInline]


admin.site.register(TargetMP)
admin.site.register(WechatArticle, WechatArticleAdmin)
admin.site.register(Comment)
