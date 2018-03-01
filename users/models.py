#coding=utf8
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    userbianhao=models.IntegerField(verbose_name=u"用户编号",default=0)
    nick_name=models.CharField(max_length=30,verbose_name=u"昵称",null=True,blank=True)
    mobile=models.CharField(max_length=11,verbose_name=u"手机号",)
    yue=models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u"余额",default=0)
    djyue=models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u"冻结余额",default=0)
    qianbao=models.CharField(max_length=42,verbose_name=u"钱包地址",null=True,blank=True)
    jihuo=models.BooleanField(default=False,verbose_name=u"激活状态")
    jingyuan=models.DecimalField(max_digits=20,decimal_places=2,verbose_name=u"精元",default=0)
    juejin=models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u"掘金和",default=0)
    count = models.IntegerField(verbose_name=u"狗狗数量",default=0)
    yaoqingrenshu = models.IntegerField(verbose_name=u"邀请人数",default=0)




    class Mate:
        verbose_name=u"用户信息"
        verbose_name_plural=verbose_name

    def __unicode__(self):
         return self.username


class YueChange(models.Model):
    user=models.ForeignKey(UserProfile,verbose_name=u"用户")
    change_to=models.CharField(max_length=42,verbose_name=u"收款方")
    change_type=models.CharField(verbose_name=u"交易类型",choices=(("tixian",u"提现"),("chongzhi",u"充值"),("zhuche",u"注册")),max_length=50)
    change_time=models.DateTimeField(verbose_name=u"交易时间",default=datetime.now)
    change_jine=models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u"交易金额")
    shifouchenggong=models.BooleanField(default=False,verbose_name=u"是否成功")


    class Meta:
        verbose_name=u"交易"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.change_type

class Sms(models.Model):
    smscode=models.CharField(max_length=6,verbose_name=u"验证码")
    mobile = models.CharField(max_length=11, verbose_name=u"手机号")
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)
    send_type = models.CharField(verbose_name=u"发送类型",default="register",choices=(("register", u"注册"), ("forget", u"忘记密码")),max_length=50)

    class Meta:
        verbose_name=u"注册验证码"
        verbose_name_plural = verbose_name


class JiaoYiJiLu(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    jiaoyi_dog = models.IntegerField(verbose_name=u"交易产生的狗" ,default=0)
    jiaoyi_type = models.CharField(verbose_name=u"交易类型",choices=(("choujiang", u"抽奖"),("weishi", u"喂食"),("juejin", u"掘金"),("maide", u"卖得"), ("maihua", u"买花"), ("shengde", u"生得"),("shenghua", u"生花")), max_length=25)
    jiaoyi_time = models.DateTimeField(verbose_name=u"交易时间", default=datetime.now)
    jiaoyi_jine=models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u"交易金额")

class YaoQing(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    yaoqing_time = models.DateTimeField(verbose_name=u"邀请时间", default=datetime.now)
    yaoqingdaouser = models.IntegerField(verbose_name=u"被邀请人",default=0)
    shifoushengxiao = models.BooleanField(default=False,verbose_name=u"是否生效")

class ChouJiang(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    choujiang_time = models.DateTimeField(verbose_name=u"抽奖时间", default=datetime.now)
    choujiang_haoma = models.IntegerField(verbose_name=u"抽奖号码",default=0)
    choujiang_jiangpin = models.CharField(verbose_name=u"抽奖奖品",max_length=25)



