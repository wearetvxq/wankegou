# coding=utf8
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class CatInfo(models.Model):
    user = models.ForeignKey('users.UserProfile', verbose_name=u"主人")
    tizhong = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u"体重",default=0)
    juejinzhi = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"掘金值", default=0)
    chengzhangzhi = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"成长值", default=0)
    shengyuzhi = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"生育值", default=0)
    daishu = models.IntegerField(verbose_name="代数")
    image = models.URLField( max_length=50,verbose_name=u"宠物图片",default='http://p2du8wu7r.bkt.clouddn.com/1.svg')
    status = models.CharField(verbose_name=u"宠物状态",choices=(("chushou",u"出售"),("shengzhi",u"生殖"),("zhengchang",u"正常")),default="zhengchang", max_length=50)
    jiage =  models.DecimalField(max_digits=20,decimal_places=2,verbose_name=u"生育出售价格",default=0)
    chushengdata = models.DateTimeField(verbose_name=u"出生时间",default=datetime.now)
    fuqingid = models.IntegerField(verbose_name=u"父亲id",default=0)
    muqingid = models.IntegerField(verbose_name=u"母亲id",default=0)
    weicishu = models.IntegerField(verbose_name=u"喂食次数",default=0)
    meitianweishi = models.DecimalField(max_digits=8, decimal_places=4, verbose_name=u"每天喂食值", default=0)
    shengcishu = models.IntegerField(verbose_name=u"生育次数",default=0)
    shengyushijian = models.DateTimeField(verbose_name=u"下次生育时间",default=datetime.now)
    dogname = models.CharField(verbose_name=u"宠物名字",max_length=30,default=1)
    xidaishu = models.DecimalField(max_digits=8, decimal_places=4, verbose_name=u"系代数", default=1)


    class Mate:
        verbose_name = u"宠物信息"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __unicode__(self):
        return self.dogname

#     是否重复


class JueJin(models.Model):
    cat = models.ForeignKey(CatInfo,verbose_name=u"猫")
    juejindata = models.DateTimeField(verbose_name=u"掘金时间",default=datetime.now)
    juejinnumber = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u"掘金数量", default=0)



class WeiShi(models.Model):
    cat = models.ForeignKey(CatInfo,verbose_name=u"猫")
    weishidata = models.DateTimeField(verbose_name=u"喂食时间",default=datetime.now)
    weishinumber = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u"喂食数量", default=0)
    weishihash = models.CharField(max_length=60,verbose_name=u"喂食hash",default=111111111111111111111111111111111111111111)
    weishizhengzhangtishu = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u"喂食增体重", default=0)
    weishizhengshuxing = models.CharField(verbose_name=u"增加属性",choices=(("tizhong",u"体重"),("shengyu",u"生育"),("juejin",u"掘金"),("weizhengjia",u"未增加")),default="weizhengjia",max_length=15)
    weishizhengshuxingzhi = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"喂食增属性值", null=True,blank=True)  #null=True,blank=True


class GouMai(models.Model):
    fuqing = models.ForeignKey('users.UserProfile', verbose_name=u"买方id")
    muqing = models.IntegerField(verbose_name=u"卖方id")
    shengyudata = models.DateTimeField(verbose_name=u"购买时间", default=datetime.now)
    shengyunumber = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"购买价格", default=0)


class ShengYu(models.Model):
    fuqing = models.ForeignKey('users.UserProfile', verbose_name=u"父亲id")
    muqing = models.IntegerField(verbose_name=u"母亲id")
    shengyudata = models.DateTimeField(verbose_name=u"生育时间", default=datetime.now)
    shengyunumber = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=u"生育价格", default=0)

