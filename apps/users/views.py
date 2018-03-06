# coding=utf8

from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from decimal import *
from market.models import CatInfo
import time
import hashlib
import re
# Create your views here.
from .models import UserProfile, YueChange, Sms, JiaoYiJiLu, YaoQing, ChouJiang
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
import random
from datetime import datetime
from yuntongxun.CCP import ccp
import logging as log
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from utils.getdog import getdogs


class CheckMovileView(View):
    def post(self, request):
        mobile = request.POST.get("mobile", "")

        if UserProfile.objects.filter(mobile=mobile):
            return JsonResponse({"code": 1, "msg": "need_login"})
        else:
            return JsonResponse({"code": 1, "msg": "need_register"})


class SendSmsView(View):
    def post(self, request):
        mobile = request.POST.get("mobile", "")
        code = "%06d" % random.randint(0, 999999)
        smscode = str(code)
        sms = Sms()
        sms.mobile = mobile
        sms.smscode = smscode
        # sms.send_time = datetime.now
        # sms.send_type = "register"
        sms.save()
        try:
            ccp.sendTemplateSMS(mobile, [smscode, 5], 232401)
        except Exception as e:
            log.error(e)
            return JsonResponse({"code": 0, "msg": "短信发送失败"})
        return JsonResponse({"code": 1, "msg": "发送成功"})


class DoLoginView(View):
    def post(self, request):
        # login_form=LoginForm(request.POST)
        # if login_form.is_valid():
        actionFlag = request.POST.get("actionflag", "")
        mobile = request.POST.get("mobile", "")
        id = request.POST.get("id", "")

        if actionFlag == 'login':
            password = request.POST.get("password", "")
            user = authenticate(username=mobile, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"code": 1, "msg": "登陆成功"})
            else:
                return JsonResponse({"code": 0, "msg": "密码错误"})
        elif actionFlag == 'register':
            password = request.POST.get("newpassword", "")
            smscode = request.POST.get("vcode", "")
            if Sms.objects.filter(smscode=smscode, mobile=mobile) or smscode == '123456':

                user_profile = UserProfile()
                user_profile.username = mobile
                user_profile.mobile = mobile
                user_profile.password = make_password(password)
                user_profile.nick_name = mobile

                user_profile.save()
                user_profile.userbianhao = user_profile.id
                user_profile.save()
                if id:
                    yaoqing = YaoQing()
                    yaoqing.user = UserProfile.objects.get(id=id)
                    yaoqing.yaoqingdaouser = user_profile.id
                    yaoqing.save()

                return JsonResponse({"code": 1, "msg": "注册成功，请激活"})
            else:
                return JsonResponse({"code": 0, "msg": "验证码错误"})


class CheckLoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            user = UserProfile.objects.get(id=request.user.id)
            conut = CatInfo.objects.filter(user=user).count()
            if user:
                users = {
                    # "id": "user.id",
                    # "yue":"user.yue",
                    # "jingyuan":"user.jingyuan",
                    # "conut" :conut,
                    # "juejin":"user.juejin",
                    #
                    #
                    # "mobile":"user.mobile",
                    # "jihuo":"user.jihuo",
                    # "qianbao": "user.qianbao",
                    # "nick_name": "user.nick_name",

                }

                return JsonResponse({"code": 1, "msg": "登陆中", "user": users})
        else:
            return JsonResponse({"code": 0, "msg": "请登陆"})


class ModifyNicknameView(View):
    def post(self, request):
        nickname = request.POST.get("nickname", "")
        user = UserProfile.objects.get(id=request.user.id)
        user.nick_name = nickname
        user.save()
        return JsonResponse({"code": 1, "msg": "修改成功", })


class RechargeView(View):
    def post(self, request):
        amount = request.POST.get("amount", "")
        user = UserProfile.objects.get(id=request.user.id)
        if user.jihuo:
            # change = YueChange.objects.get(id=request.user.id,change_jine=amount)
            # if datetime.now-change.change_time <= 3600:
            #     user.yue += amount
            yuechange = YueChange()
            yuechange.user = user
            yuechange.change_type = 'chongzhi'
            yuechange.change_jine = Decimal(amount)
            yuechange.change_to = user.qianbao
            yuechange.save()

            return JsonResponse({"code": 1, "msg": "充值", })
        else:
            return JsonResponse({"code": 0, "msg": "未绑定钱包", })


class DoBindView(View):
    def post(self, request):
        walletID = request.POST.get("walletID", "")
        code = "%06d" % random.randint(0, 999999)
        jine = "0." + str(code)

        user = UserProfile.objects.filter(qianbao=walletID).count()
        if user == 1:
            return JsonResponse({"code": 0, "msg": "此账号已绑定", })
        else:
            return JsonResponse({"code": 1, "msg": jine, })


class SubmitBindQueryView(View):
    def post(self, request):
        id = request.user.id
        walletID = request.POST.get("walletID", "")

        if UserProfile.objects.filter(qianbao=walletID).count() == 1:
            return JsonResponse({"code": 0, "msg": "该钱包以绑定过", })
        amount = request.POST.get("amount", "")
        # change = YueChange.objects.get(id=request.user.id,change_jine=amount)
        # if datetime.now-change.change_time <= 3600:
        user = UserProfile.objects.get(id=id)
        if user.jihuo:
            return JsonResponse({"code": 0, "msg": "用户已绑定，请返回用户页面刷新", })
        user.qianbao = walletID
        yuechang = YueChange()
        yuechang.user = user
        yuechang.change_type = "zhuche"
        yuechang.change_jine = Decimal(amount)
        yuechang.change_to = walletID  # 为了显示转账钱包
        yuechang.save()

        user.save()
        return JsonResponse({"code": 1, "msg": "绑定成功，请与转账五分钟之后刷新用户", })
        # return JsonResponse({"code": 1, "msg": id, })


class CheckCertifyView(View):
    def post(self, request):
        walletID = request.POST.get("walletID", "")
        trade_id = request.POST.get("trade_id", "")
        # change = YueChange.objects.get(id=request.user.id,change_jine=amount)
        # if datetime.now-change.change_time <= 3600:
        # if (data.code == 0){
        # $.toast(data.msg, "text");
        # }
        # else {
        # if (data.msg == 'success'){
        # $.alert("已认证成功");
        # location.href = '/user/index.html';
        # }
        # else if (data.msg == 'cancel'){
        # $.alert("认证已超时，请重新发起认证");
        # window.location.reload();
        # }
        # }


class LogoutView(View):

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


class SubmitWithdrawView(View):

    def post(self, request):
        id = request.user.id

        amount = request.POST.get("amount", "")
        user_profile = UserProfile.objects.get(id=id)

        # amount = Decimal(1) / Decimal(8)
        amount = float(amount)
        getcontext().prec = 8

        amount = Decimal(amount)
        if amount >= 10:
            if user_profile.jihuo:
                # return JsonResponse({"code": 0, "msg": "最低提现金未10", })
                if amount <= user_profile.yue:

                    user_profile.yue -= amount
                    user_profile.djyue += amount
                    user_profile.save()
                    change = YueChange()
                    change.user_id = user_profile.id
                    change.change_to = user_profile.qianbao
                    change.change_type = "tixian"
                    change.change_jine = amount
                    change.save()
                    return JsonResponse({"code": 1, "msg": "提现成功", })
                else:
                    return JsonResponse({"code": 0, "msg": "余额不足请重新输入", })
            else:
                return JsonResponse({"code": 0, "msg": "请先完成绑定钱包操作", })
        else:
            return JsonResponse({"code": 0, "msg": "最低提现金为10", })


class HouTaiView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)

        if user.userbianhao >= 5:
            return render(request, "fenfa.html", {"msg": "您没有权限访问此页面"})
        else:
            yuechanges = YueChange.objects.filter(shifouchenggong=False, change_type='chongzhi').order_by(
                '-change_time')[:5]
            yuechanges2 = YueChange.objects.filter(shifouchenggong=False, change_type='tixian').order_by(
                '-change_time')[:5]
            yuechanges1 = YueChange.objects.filter(shifouchenggong=False, change_type='zhuche').order_by(
                '-change_time')[:5]

            return render(request, "houtai.html",
                          {"yuechanges": yuechanges, "yuechanges2": yuechanges2, "yuechanges1": yuechanges1})

    def post(self, request):
        userlogin = UserProfile.objects.get(id=request.user.id)
        id = request.POST.get("id", "")

        if userlogin.id != 1:
            return render(request, "fenfa.html", {"msg": "您没有权限访问此页面"})
        else:
            if YueChange.objects.filter(id=id, shifouchenggong=False).count() > 0:
                if YueChange.objects.filter(id=id, change_type='chongzhi').count() > 0:
                    yuechange = YueChange.objects.get(id=id)

                    user = UserProfile.objects.get(id=yuechange.user_id)
                    user.yue += yuechange.change_jine
                    user.save()
                    yuechange.shifouchenggong = True
                    yuechange.save()
                elif YueChange.objects.filter(id=id, change_type='tixian').count() > 0:
                    yuechange = YueChange.objects.get(id=id)
                    user = UserProfile.objects.get(id=yuechange.user_id)
                    user.djyue -= yuechange.change_jine
                    user.save()
                    yuechange.shifouchenggong = True
                    yuechange.save()
                else:
                    yuechange = YueChange.objects.get(id=id)
                    user = UserProfile.objects.get(id=yuechange.user_id)
                    user.jihuo = True
                    user.save()
                    yuechange.shifouchenggong = True
                    yuechange.save()
                    if YaoQing.objects.filter(yaoqingdaouser=user.id).count() == 1:
                        yaoqing = YaoQing.objects.get(yaoqingdaouser=user.id)
                        yuanuser = UserProfile.objects.get(id=yaoqing.user_id)
                        yuanuser.yaoqingrenshu += 1
                        yaoqing.shifoushengxiao = True
                        if yuanuser.yaoqingrenshu == 5:
                            userid = yuanuser.id
                            getdogs(userid, 8)



                        elif yuanuser.yaoqingrenshu == 10:
                            userid = yuanuser.id
                            getdogs(userid, 7)

                        elif yuanuser.yaoqingrenshu == 15:
                            userid = yuanuser.id
                            getdogs(userid, 6)

                        elif yuanuser.yaoqingrenshu == 20:
                            userid = yuanuser.id
                            getdogs(userid, 5)

                        yaoqing.save()
                        yuanuser.save()



            else:

                return render(request, {"msg": "此交易以有其他管理员完成确认"})


class RecordsView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        jiaoyis = JiaoYiJiLu.objects.filter(user=user)

        return render(request, "records.html", {"jiaoyis": jiaoyis})


class WithdrawRecordsView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        yuechanges = YueChange.objects.filter(user=user)

        return render(request, "withdraw_records.html", {"yuechanges": yuechanges})


class YaoQingView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        yaoqings = YaoQing.objects.filter(user=user)

        return render(request, "yaoqingjilu.html", {"yaoqings": yaoqings})


class ChouGiangView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        choujiangs = ChouJiang.objects.all().order_by('-choujiang_time')[:5]
        count = ChouJiang.objects.all().count()
        shengyu = 500 - count

        return render(request, "choujiang.html", {"choujiangs": choujiangs, "shengyu": shengyu})

    def post(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        i = 2
        list1 = []
        while i <= 500:
            list1.append(i)
            i += 1
        if user.yue >= 10:
            if ChouJiang.objects.filter(user=user).count() == 5:
                return JsonResponse({"code": 0, "msg": "您已经参加满5次抽奖活动了，请下次再来"})
            else:

                jiaoyijilu1 = JiaoYiJiLu()
                jiaoyijilu1.user = user
                jiaoyijilu1.jiaoyi_type = 'choujiang'
                jiaoyijilu1.jiaoyi_jine = 10
                jiaoyijilu1.jiaoyi_dog = 0
                jiaoyijilu1.save()
                yiyous = ChouJiang.objects.filter(~Q(choujiang_haoma=0))

                for i in yiyous:
                    i2 = i.choujiang_haoma
                    list1.remove(i2)

                list = random.sample(list1, 1)

                a1 = list[0]

                a2 = int(a1)
                choujiang = ChouJiang()

                if a2 >= 400:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'jingyuan'
                    choujiang.user = user

                    choujiang.save()
                    user.yue -= 10
                    user.jingyuan += 10
                    user.save()
                    return JsonResponse({"code": 1, "msg": "恭喜您活动十精元"})
                elif a2 >= 300:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'jiudai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 9)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得九代狗狗一只"})
                elif a2 >= 200:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'badai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 8)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得八代狗狗一只"})
                elif a2 >= 150:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'qidai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()

                    userid = user.id

                    getdogs(userid, 7)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得七代狗狗一只"})
                elif a2 >= 100:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'liudai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 6)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得六代狗狗一只"})
                elif a2 >= 75:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'wudai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 5)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得五代狗狗一只"})
                elif a2 >= 50:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'sidai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    userid = user.id

                    getdogs(userid, 4)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得四代狗狗一只"})
                elif a2 >= 25:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'sandai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 3)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得三代狗狗一只"})
                elif a2 >= 10:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'erdai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 2)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得二代狗狗一只"})
                elif a2 >= 2:
                    choujiang.choujiang_haoma = a2
                    choujiang.choujiang_jiangpin = 'yidai'
                    choujiang.user = user
                    choujiang.save()
                    user.yue -= 10
                    user.save()
                    userid = user.id

                    getdogs(userid, 1)
                    return JsonResponse({"code": 1, "msg": "恭喜您获得一代狗狗一只"})








        else:
            return JsonResponse({"code": 0, "msg": "余额不足，请先充值哦"})


class GetDogView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        mobile = request.GET.get("mobile", "-1")
        daishu = request.GET.get("daishu", "-1")

        if user.id != 1:
            return render(request, "fenfa.html", {"msg": "您没有权限访问此页面"})

        else:

            user0 = UserProfile.objects.get(mobile=mobile)
            userid = user0.id
            getdogs(userid, daishu)

            return render(request, "fenfa.html", {"msg": "发放成功"})


class ShanChuQianBaoView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        user.jihuo = False
        user.qianbao = ''
        user.save()

        return render(request, "user.html")
