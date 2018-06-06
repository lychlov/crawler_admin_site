from django.contrib import admin
from .models import TargetMP, WechatArticle


# Register your models here.
class WechatArticleAdmin(admin.ModelAdmin):
    list_display = ('account', 'tittle', 'summary', 'url', 'recieve_time')
    list_filter = ['recieve_time', 'account']


admin.site.register(TargetMP)
admin.site.register(WechatArticle, WechatArticleAdmin)
