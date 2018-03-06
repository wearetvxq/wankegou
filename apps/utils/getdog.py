#coding=utf8


# 独立使用django的model
import sys
import os

# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wanke.settings")

import django

django.setup()


from users.models import UserProfile



from market.models import CatInfo
import time
import hashlib
import re
# Create your views here.


from datetime import datetime

from decimal import *

import logging as log
def getdogs(userid,daishu):
    user0=UserProfile.objects.get(id=userid)

    user0.count += 1
    user0.save()
    nowdog = CatInfo()
    nowdog.user = user0
    nowdog.daishu = daishu


    if nowdog.daishu == 1:
        nowdog.xidaishu = 1.15
    elif nowdog.daishu == 0:
        nowdog.xidaishu = 1
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

    nowdog.save()

    return nowdog.id

if __name__ == '__main__':
    getdogs(1,0)