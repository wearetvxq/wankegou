#coding=utf-8
__auth__ = 'huwei'
__date__ = '2017/4/12 14:12'

import xadmin
from xadmin import views
from .models import YueChange,ChouJiang,UserProfile
from django.contrib.auth.models import User
from xadmin.plugins.auth import UserAdmin



class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GlobalSettings(object):
    site_title="青蛙dog后台管理"
    site_footer="青蛙dog"
    menu_style="accordion"



class UserProfileAdmin(UserAdmin):
    list_display=['userbianhao','mobile','yue','djyue','jihuo','count','qianbao']
    search_fields=['userbianhao','mobile','yue','djyue','jihuo','count','qianbao']
    list_filter=['userbianhao','mobile','yue','djyue','jihuo','count','qianbao']

class YueChangeAdmin(object):
    list_display=['change_to','change_type','change_time','change_jine']
    search_fields=['change_to','change_type','change_time','change_jine']
    list_filter=['change_to','change_type','change_time','change_jine']


class ChouJiangAdmin(object):
    list_display=['choujiang_time','choujiang_haoma','choujiang_jiangpin']
    search_fields=['choujiang_time','choujiang_haoma','choujiang_jiangpin']
    list_filter=['choujiang_time','choujiang_haoma','choujiang_jiangpin']








xadmin.site.unregister(UserProfile)

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(YueChange,YueChangeAdmin)
xadmin.site.register(ChouJiang,ChouJiangAdmin)
xadmin.site.register(UserProfile,UserProfileAdmin)



