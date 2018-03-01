#coding=utf8
import xadmin
from xadmin import views
from .models import CatInfo ,JueJin,WeiShi,ShengYu


class CatInfoAdmin(object):
    list_display=['id','user','dogname','tizhong','juejinzhi','chengzhangzhi','shengyuzhi','daishu','image','status','jiage','chushengdata','fuqingid','muqingid']
    search_fields=['id','user','dogname','tizhong','juejinzhi','chengzhangzhi','shengyuzhi','daishu','image','status','jiage','chushengdata','fuqingid','muqingid']
    list_filter=['id','user','dogname','tizhong','juejinzhi','chengzhangzhi','shengyuzhi','daishu','image','status','jiage','chushengdata','fuqingid','muqingid']


class JueJinAdmin(object):
    list_display=['cat','juejindata','juejinnumber']
    search_fields=['cat','juejindata','juejinnumber']
    list_filter=['cat','juejindata','juejinnumber']

class WeiShiAdmin(object):
    list_display=['cat','weishidata','weishinumber','weishihash']
    search_fields=['cat','weishidata','weishinumber','weishihash']
    list_filter=['cat','weishidata','weishinumber','weishihash']

class ShengYuAdmin(object):
    list_display=['fuqing','muqing','shengyudata','shengyunumber','zinv']
    search_fields=['fuqing','muqing','shengyudata','shengyunumber','zinv']
    list_filter=['fuqing','muqing','shengyudata','shengyunumber','zinv']





xadmin.site.register(CatInfo,CatInfoAdmin)
xadmin.site.register(JueJin,JueJinAdmin)
xadmin.site.register(WeiShi,WeiShiAdmin)
xadmin.site.register(ShengYu,ShengYuAdmin)



