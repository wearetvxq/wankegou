# coding=utf8

from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from decimal import *
from django.db.models import Q

# Create your views here.
from users.models import UserProfile, YueChange, Sms, JiaoYiJiLu, ChouJiang
from .models import CatInfo, JueJin, WeiShi
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
import random
from datetime import datetime
from yuntongxun.CCP import ccp
import logging as log
import time
import hashlib
import re
from login import LoginRequiredMixin
from django.contrib.auth.hashers import make_password, check_password


#
# class CheckMovileView(View):
#     def post(self, request):
#         mobile = request.POST.get("mobile", "")
#         if UserProfile.objects.filter(mobile=mobile):
#             return JsonResponse({"code":1,"msg":"need_login"})
#         else:
#             return JsonResponse({"code":1,"msg":"need_register"})

class HomePageView(View):
    def get(self, request):
        type = int(request.GET.get("type", "1"))
        dai = request.GET.get("dai", "-1")
        id = int(request.GET.get("id", "-1"))
        if type == 1:
            # dog = CatInfo.objects.filter(~Q(chushoujiage="")).order_by("-chushoujiage")  # filter(filedname__isnull=Flase)
            dog_list = CatInfo.objects.filter(status="chushou").order_by('jiage')[:30]
            if dai >= '0':
                dog_list = CatInfo.objects.filter(status="chushou", daishu=dai).order_by('jiage')[:30]
            if id >= 0:
                dog_list = CatInfo.objects.filter(status="chushou", id=id).order_by('jiage')[:30]
        #
        #
        else:
            dog_list = CatInfo.objects.filter(status="shengzhi").order_by('jiage')[:30]
            if dai >= '0':
                dog_list = CatInfo.objects.filter(status="shengzhi", daishu=dai).order_by('jiage')[:30]
            if id >= 0:
                dog_list = CatInfo.objects.filter(status="shengzhi", id=id).order_by('jiage')[:30]

        dogs = []
        if dog_list:
            for dog in dog_list:
                dogx = {
                    "id": dog.id,
                    "jiage": dog.jiage,
                    "tizhong": dog.tizhong,
                    "chengzhangzhi": dog.chengzhangzhi,
                    "shengyuzhi": dog.shengyuzhi,  # 将返回的Datatime类型格式化为字符串
                    "juejinzhi": dog.juejinzhi,
                    "daishu": dog.daishu,
                    "image": str(dog.image),
                    "status": dog.status
                }
                dogs.append(dogx)

            return JsonResponse({"code": 1, "msg": dogs})


        else:
            return JsonResponse({"code": 0, "msg": '未找到合适的宠物1'})

    def post(self, request):
        data = '''

                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>

                <div id="list"   data-v-f1666576="" class="item" onclick="bearurl(9875);"><div data-v-f1666576="" class="img"><img data-v-f1666576="" src="http://p2du8wu7r.bkt.clouddn.com/59.svg" style="background: rgb(255, 232, 252);"><div data-v-f1666576="" class="id"># 9875</div><div data-v-f1666576="" class="gen">17代</div><div data-v-f1666576="" class="info"><p data-v-f1666576="">0次</p><p data-v-f1666576="">1.6/1.7/1.9•0kg</p></div></div><div data-v-f1666576="" class="price"><i data-v-f1666576="" class="ico sell"></i><span data-v-f1666576="">1 wkc</span></div></div>
        '''

        dog_list = CatInfo.objects.filter(status="shengzhi").order_by('jiage')[:30]

        dogs = []
        if dog_list:
            for dog in dog_list:
                dogx = {
                    "id": dog.id,
                    "jiage": dog.jiage,
                    "tizhong": dog.tizhong,
                    "chengzhangzhi": dog.chengzhangzhi,
                    "shengyuzhi": dog.shengyuzhi,  # 将返回的Datatime类型格式化为字符串
                    "juejinzhi": dog.juejinzhi,
                    "daishu": dog.daishu,
                    "image": str(dog.image),
                    "status": dog.status
                }
                dogs.append(dogx)
        # return JsonResponse({"code": 0, "msg2": data, "msg": dogs})
        return JsonResponse({"code": 0, "msg2": data})

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        num = CatInfo.objects.filter(user=user.id).count()
        dogs = CatInfo.objects.filter(user=user.id)

        dogs1 = []
        if dogs:
            for dog in dogs:
                dog = {
                    "id": dog.id,
                    "jiage": dog.jiage,
                    "tizhong": dog.tizhong,
                    "chengzhangzhi": dog.chengzhangzhi,
                    "shengyuzhi": dog.shengyuzhi,  # 将返回的Datatime类型格式化为字符串
                    "juejinzhi": dog.juejinzhi,
                    "daishu": dog.daishu,
                    "image": str(dog.image),
                    "status": dog.status,
                    "shengyushijian": time.mktime(dog.shengyushijian.timetuple()),
                    "weicishu": dog.weicishu,
                    "shengcishu": dog.shengcishu,
                    "meitianweishi": dog.meitianweishi

                }
                dogs1.append(dog)

        return render(request, "home.html", {"dogs": dogs1, "num": num})


class DogInfoView(LoginRequiredMixin, View):
    def get(self, request):
        id = int(request.GET.get("id", "-1"))
        user = UserProfile.objects.get(id=request.user.id)
        dog = CatInfo.objects.get(id=id)
        if user.id == dog.user_id:
            if dog.status == 'chushou':
                xid = "110"
            elif dog.status == 'shengzhi':
                xid = "101"
            else:
                xid = "100"

        else:
            if dog.status == 'chushou':
                xid = "010"
            elif dog.status == 'shengzhi':
                xid = "001"
            else:
                xid = "000"

        # xid = '110'  #1主人100 2-110  3-101  4非出/生000  010

        juejin = JueJin.objects.filter(cat=id).order_by("-juejindata")
        weishi = WeiShi.objects.filter(cat=id).order_by("-weishidata")
        juejinall = 0
        for i in juejin:
            juejinall += i.juejinnumber

        if dog:
            dogs = {
                "id": dog.id,
                "jiage": dog.jiage,
                "tizhong": dog.tizhong,
                "chengzhangzhi": dog.chengzhangzhi,
                "shengyuzhi": dog.shengyuzhi,  # 将返回的Datatime类型格式化为字符串
                "juejinzhi": dog.juejinzhi,
                "daishu": dog.daishu,
                "image": str(dog.image),
                "status": dog.status,
                "shengyushijian": time.mktime(dog.shengyushijian.timetuple()),
                "weicishu": dog.weicishu,
                "shengcishu": dog.shengcishu,
                "fuqingid": dog.fuqingid,
                "chushengdata": dog.chushengdata,
                "muqingid": dog.muqingid,
                "username": dog.user.nick_name,
                "meitianweishi": dog.meitianweishi,
            }

        return render(request, "doginfo.html", {"dog": dogs,
                                                "xid": xid,
                                                "juejin": juejin,
                                                "weishi": weishi,
                                                "juejinall": juejinall,

                                                })


class UnSellView(View):
    def get(self, request):
        id = int(request.GET.get("id", "-1"))  # 宠物id
        user = UserProfile.objects.get(id=request.user.id)
        type = int(request.GET.get("type", "-1"))  # 1发起  2是撤回
        type2 = int(request.GET.get("type2", "-1"))  # 1出售  2生育
        money = Decimal(request.GET.get("money", "0"))  # 金额
        password = request.GET.get("pass", "-1")
        yajin = money * Decimal(0.03)
        if authenticate(username=user.username, password=password):
            if type == 1 and type2 == 1:
                if yajin > user.yue:
                    return JsonResponse({"code": 0, "msg": "余额不足以支付押金 请先充值"})

                dog = CatInfo.objects.get(id=id)
                if dog.daishu == 0:
                    return JsonResponse({"code": 0, "msg": "0代狗不允许交易哦"})
                dog.status = 'chushou'
                dog.jiage = money
                dog.save()
                user.yue = user.yue - Decimal(yajin)
                user.djyue = user.djyue + Decimal(yajin)
                user.save()
                return JsonResponse({"code": 1, "msg": "出售挂单成功"})

            elif type == 2 and type2 == -1:
                dog = CatInfo.objects.get(id=id)
                money = dog.jiage  # 1  bug
                yajin = money * Decimal(0.03)
                dog.status = 'zhengchang'
                dog.jiage = '0'
                dog.save()

                user.yue = user.yue + Decimal(yajin)
                user.djyue = user.djyue - Decimal(yajin)
                user.save()
                return JsonResponse({"code": 1, "msg": "取消出售"})
            elif type == 1 and type2 == 2:
                if yajin > user.yue:
                    return JsonResponse({"code": 0, "msg": "余额不足以支付押金 请先充值"})
                dog = CatInfo.objects.get(id=id)
                if dog.daishu < 6:
                    if dog.shengyushijian < datetime.now():
                        dog.status = 'shengzhi'
                        dog.jiage = money
                        dog.save()
                        user.yue = user.yue - Decimal(yajin)
                        user.djyue = user.djyue + Decimal(yajin)
                        user.save()
                        return JsonResponse({"code": 1, "msg": "生育挂单成功"})
                    else:
                        return JsonResponse({"code": 0, "msg": "狗狗生育冷却中"})
                else:
                    return JsonResponse({"code": 0, "msg": "目前只有五代以上的狗狗能生育小狗哦"})
        else:
            return JsonResponse({"code": 0, "msg": "密码错误，请重新操作"})


class BuyView(View):
    def post(self, request):  # 因为涉及密码 所以先post
        id = int(request.POST.get("id", "-1"))  # 宠物id
        user = UserProfile.objects.get(id=request.user.id)
        type = int(request.POST.get("type", "-1"))
        password = request.POST.get("pass", "-1")
        myDogId = int(request.POST.get("myDogId", "-1"))
        if authenticate(username=user.username, password=password):

            return JsonResponse({"code": "1", "id": id, "myDogId": myDogId, "msg": "成功登陆"})
        #     没有 验证余额

        else:
            return JsonResponse({"code": 0, "msg": "密码错误，请重新操作"})

    def get(self, request):
        id = int(request.GET.get("id", "-1"))  # 宠物id
        user = UserProfile.objects.get(id=request.user.id)
        myDogId = int(request.GET.get("mydogid", "-1"))
        dog = CatInfo.objects.get(id=id)
        if dog:
            dogs = {
                "id": dog.id,
                "jiage": dog.jiage,
                "tizhong": dog.tizhong,
                "chengzhangzhi": dog.chengzhangzhi,
                "shengyuzhi": dog.shengyuzhi,  # 将返回的Datatime类型格式化为字符串
                "juejinzhi": dog.juejinzhi,
                "daishu": dog.daishu,
                "image": str(dog.image),
                "status": dog.status,
                "shengyushijian": time.mktime(dog.shengyushijian.timetuple()),
                "weicishu": dog.weicishu,
                "shengcishu": dog.shengcishu,
                "fuqingid": dog.fuqingid,
                "chushengdata": dog.chushengdata,
                "muqingid": dog.muqingid,
                "username": dog.user.nick_name,
                "meitianweishi": dog.meitianweishi,
            }

        if myDogId == -1:
            type = -1
        else:
            type = int(myDogId)

        # id = 2 & mydogid = -1
        return render(request, "buy.html", {
            'dog': dogs,
            'type': type,
        })


class GetMydogView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        dogs = CatInfo.objects.filter(user=user, status="zhengchang")

        #
        data = []
        if dogs:
            for dog in dogs:
                if dog.shengyushijian <= datetime.now():
                    if dog.daishu <= 5:
                        text = str(dog.daishu) + "代 ID:#" + str(dog.id)
                        dog = {
                            "value": dog.id,

                            "text": text,

                        }
                        data.append(dog)

        if data:
            return JsonResponse({"code": '1', "dogs": data})
        else:
            return JsonResponse({"code": '0'})


class GetNowdogView(View):
    def post(self, request):

        id = int(request.POST.get("id", "-1"))  # 宠物id
        user = UserProfile.objects.get(id=request.user.id)
        type = int(request.POST.get("type", "-1"))
        dog = CatInfo.objects.get(id=id)
        yuanzhuren = dog.user_id
        yuanuser = UserProfile.objects.get(id=yuanzhuren)
        yajin2 = int(dog.jiage) * 0.03
        yajin = Decimal(yajin2, 8).quantize(Decimal('000.00'))
        jiage = Decimal(dog.jiage)
        if dog.status == 'zhengchang':
            return JsonResponse({"code": '0', "msg": "此交易已完成"})
        elif user.id == dog.user_id:
            return JsonResponse({"code": '0', "msg": "不能购买自己的宠物哦"})
        else:
            if user.yue > Decimal(dog.jiage):

                if type == -1:
                    # dog 是自己的

                    dog.user = user
                    user.yue = user.yue - jiage
                    user.count += 1
                    yuanuser.yue = yuanuser.yue + jiage
                    yuanuser.djyue = yuanuser.djyue - yajin
                    yuanuser.count -= 1
                    dog.status = 'zhengchang'
                    dog.jiage = '0'
                    dog.save()
                    user.save()
                    yuanuser.save()
                    jiaoyijilu1 = JiaoYiJiLu()
                    jiaoyijilu1.user = user
                    jiaoyijilu1.jiaoyi_type = 'maihua'
                    jiaoyijilu1.jiaoyi_jine = jiage
                    jiaoyijilu1.jiaoyi_dog = dog.id
                    jiaoyijilu1.save()
                    jiaoyijilu2 = JiaoYiJiLu()
                    jiaoyijilu2.user = yuanuser
                    jiaoyijilu2.jiaoyi_type = 'maide'
                    jiaoyijilu2.jiaoyi_jine = jiage
                    jiaoyijilu2.jiaoyi_dog = dog.id
                    jiaoyijilu2.save()
                    gm = UserProfile.objects.get(id=1)
                    gm.yue += yajin
                    gm.save()

                    return JsonResponse({"code": '1', "id": id, "msg": "购买成功"})
                else:
                    now1 = datetime.now()
                    fnow = time.mktime(now1.timetuple())
                    mnow = time.mktime(now1.timetuple())
                    if dog.shengcishu == 0:

                        xidaishucishujiacheng = ((Decimal(0.5) * (1 + dog.xidaishu)) / dog.shengyuzhi) * Decimal(3600)
                    else:
                        xidaishucishujiacheng = ((Decimal(0.5) * (1 + dog.xidaishu)) / dog.shengyuzhi) * Decimal(3600)
                        for i in (1, dog.shengcishu):
                            xidaishucishujiacheng = xidaishucishujiacheng * (1 + dog.xidaishu)

                    flengqueshijian = xidaishucishujiacheng
                    fnowint = int(fnow)
                    fnexttime1 = fnowint + int(flengqueshijian)
                    # 转换成localtime
                    ftime_local = time.localtime(fnexttime1)
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    fnexttime = time.strftime("%Y-%m-%d %H:%M:%S", ftime_local)
                    dog.shengyushijian = fnexttime

                    mudog = CatInfo.objects.get(id=type)
                    if mudog.shengcishu == 0:

                        muxidaishucishujiacheng = ((Decimal(0.5) * Decimal(
                            1 + mudog.xidaishu)) / mudog.shengyuzhi) * Decimal(3600)
                    else:
                        muxidaishucishujiacheng = ((Decimal(0.5) * Decimal(
                            1 + mudog.xidaishu)) / mudog.shengyuzhi) * Decimal(3600)
                        for i in (1, dog.shengcishu):
                            muxidaishucishujiacheng = muxidaishucishujiacheng * (1 + dog.xidaishu)
                    mlengqueshijian = muxidaishucishujiacheng
                    mnowint = int(mnow)
                    mnexttime1 = mnowint + int(mlengqueshijian)
                    # 转换成localtime
                    mtime_local = time.localtime(mnexttime1)
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    mnexttime = time.strftime("%Y-%m-%d %H:%M:%S", mtime_local)
                    mudog.shengyushijian = mnexttime
                    mudog.status = 'zhengchang'
                    dog.status = 'zhengchang'
                    dog.shengcishu += 1
                    mudog.shengcishu += 1

                    user.yue = user.yue - jiage
                    user.count += 1
                    yuanuser.yue = yuanuser.yue + jiage
                    yuanuser.djyue = yuanuser.djyue - yajin
                    nowdog = CatInfo()
                    nowdog.user = user
                    if dog.daishu == 0:
                        nowdog.daishu = mudog.daishu + 1
                    if mudog.daishu == 0:
                        nowdog.daishu = dog.daishu + 1
                    else:
                        nowdog.daishu = int(dog.daishu) + int(mudog.daishu)

                    if nowdog.daishu == 1:
                        nowdog.xidaishu = 1.15
                    elif nowdog.daishu == 2:
                        nowdog.xidaishu = 1.3225
                    elif nowdog.daishu == 3:
                        nowdog.xidaishu = 1.5208
                    elif nowdog.daishu == 4:
                        nowdog.xidaishu = 1.7490
                    elif nowdog.daishu == 5:
                        nowdog.xidaishu = 2.0113
                    elif nowdog.daishu == 6:
                        nowdog.xidaishu = 2.313
                    elif nowdog.daishu == 7:
                        nowdog.xidaishu = 2.66
                    elif nowdog.daishu == 8:
                        nowdog.xidaishu = 3.059
                    elif nowdog.daishu == 9:
                        nowdog.xidaishu = 3.5178
                    else:
                        nowdog.xidaishu = 4.0455

                    nowdog.fuqingid = dog.id
                    nowdog.muqingdi = mudog.id
                    nowdog.save()
                    nowid = nowdog.id
                    nowdog.image = 'http://p2du8wu7r.bkt.clouddn.com/%s.svg' % nowid
                    nowdog.dogname = nowid

                    now1 = datetime.now()
                    fnow = str(time.mktime(now1.timetuple()))
                    shuxing = hashlib.sha224(fnow).hexdigest()
                    tz1 = re.findall(r'\d+', shuxing)[-1]
                    sx1 = re.findall(r'\d+', shuxing)[0]
                    tz = int(re.findall(r'\d?', tz1)[-2])
                    sx = int(re.findall(r'\d?', sx1)[0])
                    a = str(tz * sx)

                    a2 = int(re.findall(r'\d?', a)[0])

                    nowdog.chengzhangzhi = Decimal((10 + tz) * 0.1).quantize(Decimal('00.00'))
                    nowdog.shengyuzhi = Decimal((10 + a2) * 0.1).quantize(Decimal('00.00'))
                    nowdog.juejinzhi = Decimal((10 + sx) * 0.1).quantize(Decimal('00.00'))

                    nowdog.save()

                    now1 = datetime.now()
                    nnow = time.mktime(now1.timetuple())
                    try:
                        nxidaishucishujiacheng = ((Decimal(0.5) * Decimal(
                            1 + nowdog.xidaishu)) / nowdog.shengyuzhi) * Decimal(3600)

                    except Exception as e:
                        log.error(e)

                    nlengqueshijian = nxidaishucishujiacheng
                    nnowint = int(nnow)
                    nnexttime1 = nnowint + int(nlengqueshijian)
                    # 转换成localtime
                    ntime_local = time.localtime(nnexttime1)
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    nnexttime = time.strftime("%Y-%m-%d %H:%M:%S", ntime_local)
                    nowdog.shengyushijian = nnexttime

                    jiaoyijilu1 = JiaoYiJiLu()
                    jiaoyijilu1.user = user
                    jiaoyijilu1.jiaoyi_type = 'shenghua'
                    jiaoyijilu1.jiaoyi_jine = jiage
                    jiaoyijilu1.jiaoyi_dog = dog.id
                    jiaoyijilu1.save()
                    jiaoyijilu2 = JiaoYiJiLu()
                    jiaoyijilu2.user = yuanuser
                    jiaoyijilu2.jiaoyi_type = 'shengde'
                    jiaoyijilu2.jiaoyi_jine = jiage
                    jiaoyijilu2.jiaoyi_dog = dog.id
                    jiaoyijilu2.save()
                    gm = UserProfile.objects.get(id=1)
                    gm.yue += yajin
                    gm.save()

                    dog.save()
                    mudog.save()
                    nowdog.save()
                    user.save()
                    yuanuser.save()
                    return JsonResponse({"code": '1', "id": nowid})



            else:
                return JsonResponse({"code": '0', "msg": "余额不足，请先充值"})


class WeiShiView(View):
    def get(self, request):
        id = int(request.GET.get("id", "-1"))  # 宠物id
        weishi = Decimal(request.GET.get("weishi", "-1"))
        user = UserProfile.objects.get(id=request.user.id)
        dog = CatInfo.objects.get(id=id)
        zhengshuxing = (weishi / Decimal(10)).quantize(Decimal('0.00'))
        if weishi <= user.yue:
            if dog.meitianweishi + weishi <= 5:
                if weishi >= 1:
                    dog.meitianweishi += weishi
                    weishijilu = WeiShi()
                    weishijilu.cat = dog
                    weishijilu.weishinumber = weishi
                    now1 = datetime.now()
                    fnow = str(time.mktime(now1.timetuple()))
                    weishijilu.weishihash = hashlib.sha224(fnow).hexdigest()
                    tz1 = re.findall(r'\d+', weishijilu.weishihash)[-1]
                    sx1 = re.findall(r'\d+', weishijilu.weishihash)[0]
                    tz = int(re.findall(r'\d?', tz1)[-2])
                    sx = int(re.findall(r'\d?', sx1)[0])

                    if tz in [0, 4, 7]:

                        weishijilu.weishizhengzhangtishu = weishi * dog.chengzhangzhi * Decimal(0.5)
                    elif tz == 6:
                        weishijilu.weishizhengzhangtishu = weishi * dog.chengzhangzhi * Decimal(2)
                    else:
                        weishijilu.weishizhengzhangtishu = weishi * dog.chengzhangzhi
                    dog.tizhong += weishijilu.weishizhengzhangtishu

                    c1 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[-2])  # 后一位
                    c0 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[0])  # 第一位

                    s1 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[-2])  # 后一位
                    s0 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[0])  # 后一位

                    j1 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[-2])  # 后一位
                    j0 = int(re.findall(r'\d?', str(dog.chengzhangzhi))[0])  # 后一位

                    if sx + c0 == c1 or sx + c0 - 10 == c1:
                        weishijilu.weishizhengshuxing = 'tizhong'
                        weishijilu.weishizhengshuxingzhi = zhengshuxing
                        dog.chengzhangzhi += zhengshuxing
                    elif sx + s0 == s1 or sx + s0 - 10 == s1:
                        weishijilu.weishizhengshuxing = 'shengyu'
                        weishijilu.weishizhengshuxingzhi = zhengshuxing
                        dog.shengyuzhi += zhengshuxing
                    elif sx + j0 == j1 or sx + j0 - 10 == j1:
                        weishijilu.weishizhengshuxing = 'juejin'
                        weishijilu.weishizhengshuxingzhi = zhengshuxing
                        dog.juejinzhi += zhengshuxing
                    else:
                        weishijilu.weishizhengshuxing = 'weizhengjia'
                        weishijilu.weishizhengshuxingzhi = 0

                    # 喂食记录  交易记录
                    jiaoyijilu = JiaoYiJiLu()
                    jiaoyijilu.user = user
                    jiaoyijilu.jiaoyi_type = 'weishi'
                    jiaoyijilu.jiaoyi_jine = weishi
                    jiaoyijilu.jiaoyi_dog = int(dog.id)
                    jiaoyijilu.save()

                    dog.save()
                    weishijilu.save()

                    user.yue -= weishi
                    user.save()
                    return JsonResponse({"code": '1', "msg": "喂食成功"})
                else:
                    return JsonResponse({"code": '1', "msg": "喂食金额必须大于1"})
            else:
                return JsonResponse({"code": '0', "msg": "今日喂食过多 请明日再喂"})

        else:
            return JsonResponse({"code": '0', "msg": "余额不足，请先充值"})


class FenFaGueGinView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        choujiang = ChouJiang.objects.all().count()
        jiangchi = user.yue + Decimal(choujiang * 5)
        jinriweishi = 0
        jinriquanzhi = 0

        if user.id != 1:
            return render(request, "fenfa.html", {"msg": "您没有权限访问此页面"})

        else:
            dogs = CatInfo.objects.filter(~Q(meitianweishi=0))

            for dog in dogs:
                jiangchi += dog.meitianweishi
                jinriweishi += dog.meitianweishi
                jinriquanzhi += dog.tizhong * dog.juejinzhi * dog.meitianweishi / dog.xidaishu

            jiangchi = jiangchi * Decimal(0.95)
            for dog in dogs:
                juejinnum = jiangchi / jinriquanzhi * (dog.tizhong * dog.juejinzhi * dog.meitianweishi / dog.xidaishu)

                juejin = JueJin()
                juejin.cat = dog
                juejin.juejinnumber = juejinnum
                juejin.save()

                doguser = UserProfile.objects.get(id=dog.user_id)
                doguser.yue += juejinnum
                doguser.juejin += juejinnum
                doguser.save()
                dog.meitianweishi = Decimal(0)
                dog.save()

                jiaoyijilu = JiaoYiJiLu()
                jiaoyijilu.user = doguser
                jiaoyijilu.jiaoyi_dog = dog.id
                jiaoyijilu.jiaoyi_jine = juejinnum
                jiaoyijilu.jiaoyi_type = 'juejin'
                jiaoyijilu.save()
            return render(request, "fenfa.html", {"msg": "掘金分发完成",
                                                  "weishi": jinriweishi,
                                                  "jiangchi": jiangchi,
                                                  "jinriquanzhi": jinriquanzhi,

                                                  })
