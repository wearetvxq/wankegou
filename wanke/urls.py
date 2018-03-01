# coding=utf8
from django.conf.urls import url

from users.views import CheckMovileView,DoLoginView,SendSmsView,CheckLoginView,ModifyNicknameView,ShanChuQianBaoView
from users.views import RechargeView,DoBindView,SubmitBindQueryView,CheckCertifyView,YaoQingView,Get0DaiDogView
from users.views import Get1DaiDogView,Get2DaiDogView,Get3DaiDogView,Get4DaiDogView,Get5DaiDogView
from users.views import LogoutView,SubmitWithdrawView,HouTaiView,RecordsView,WithdrawRecordsView,ChouGiangView
from market.views import HomePageView,HomeView,DogInfoView,UnSellView,BuyView,GetMydogView,GetNowdogView,WeiShiView,FenFaGueGinView

import xadmin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^login', TemplateView.as_view(template_name="login.html"), name="login"),
    url(r'^user$', TemplateView.as_view(template_name="user.html"), name="user"),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^help$', TemplateView.as_view(template_name="help.html"), name="help"),
    url(r'^ready$', TemplateView.as_view(template_name="ready.html"), name="ready"),
    url(r'^terms$', TemplateView.as_view(template_name="terms.html"), name="terms"),
    url(r'^bind$', TemplateView.as_view(template_name="bind.html"), name="bind"),
    url(r'^marketindex$', TemplateView.as_view(template_name="marketindex.html"), name="marketindex"),
    # url(r'^choujiang$', TemplateView.as_view(template_name="choujiang.html"), name="choujiang"),
    url(r'^ceshi$', TemplateView.as_view(template_name="ceshi.html"), name="ceshi"),

    # url(r'^cat/(?P<id>\d+)$', TemplateView.as_view(template_name="cat.html"), name="cat"),
    # url(r'^buy$', TemplateView.as_view(template_name="buy.html"), name="buy"),
    url(r'^market$', TemplateView.as_view(template_name="market.html"), name="market"),
    # url(r'^home$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^withdraw_records$', WithdrawRecordsView.as_view(), name="withdraw_records"),
    url(r'^records$', RecordsView.as_view(), name="records"),


    # url(r'^buy$', TemplateView.as_view(template_name="buy.html"), name="buy"),
    url(r'^doginfo$', DogInfoView.as_view(), name="doginfo"),
    url(r'^home$', HomeView.as_view(), name="home"),
    url(r'^buy', BuyView.as_view(), name="buy"),
    url(r'^houtai$', HouTaiView.as_view(), name="houtai"),
    # 狗 考虑中
    # url(r'^homedog$', TemplateView.as_view(template_name="homedog.html"), name="homedog"),
    # url(r'^userdog$', TemplateView.as_view(template_name="userdog.html"), name="userdog"),
    # url(r'^market1dog$', TemplateView.as_view(template_name="market1dog.html"), name="market1dog"),
    # url(r'^market2dog$', TemplateView.as_view(template_name="market2dog.html"), name="market2dog"),

    # url(r'^$', UserIndexView.as_view(), name="user_index"),
    # url(r'^login/$', UserLoginView.as_view(), name="user_login"),
    # url(r'^logout/', LogOutView.as_view(), name="user_logout"),
    url(r'^api/check_mobile', CheckMovileView.as_view(), name="check_mobile"),
    url(r'^api/do_login', DoLoginView.as_view(), name="do_login"),
    url(r'^api/send_sms', SendSmsView.as_view(), name="send_sms"),
    url(r'^api/check_login', CheckLoginView.as_view(), name="check_login"),
    url(r'^api/modify_nickname', ModifyNicknameView.as_view(), name="modify_nickname"),
    url(r'^api/recharge', RechargeView.as_view(), name="recharge"),
    url(r'^api/do_bind', DoBindView.as_view(), name="do_bind"),
    url(r'^api/submit_bind_query', SubmitBindQueryView.as_view(), name="submit_bind_query"),
    url(r'^api/check_certify', CheckCertifyView.as_view(), name="check_certify"),
    url(r'^api/logout', LogoutView.as_view(), name="logout"),
    url(r'^api/submit_withdraw', SubmitWithdrawView.as_view(), name="submit_withdraw"),
    url(r'^yaoqing', YaoQingView.as_view(), name="yaoqing"),

    # url(r'^market', MarketView.as_view(), name="market"),
    url(r'^api/homepage', HomePageView.as_view(), name="homepage"),

    url(r'^api/unsell', UnSellView.as_view(), name="unsell"),


    url(r'^api/getmydog', GetMydogView.as_view(), name="getmydog"),
    url(r'^api/getnowdog', GetNowdogView.as_view(), name="getnowdog"),
    url(r'^api/weishi', WeiShiView.as_view(), name="weishi"),
    # url(r'^jihuo/$', JiHuoView.as_view(), name="user_jihuo"),
    # url(r'^jihuo/jh(?P<id>\d+)', JHView.as_view(), name="user_jh"),
    url(r'^api/fenfajuejin', FenFaGueGinView.as_view(), name="fenfajuejin"),
    url(r'^choujiang', ChouGiangView.as_view(), name="choujiang"),
    url(r'^api/get0daidog',Get0DaiDogView.as_view(), name="get0daidog"),
    url(r'^api/get1daidog',Get1DaiDogView.as_view(), name="get1daidog"),
    url(r'^api/get2daidog',Get2DaiDogView.as_view(), name="get2daidog"),
    url(r'^api/get3daidog',Get3DaiDogView.as_view(), name="get3daidog"),
    url(r'^api/get4daidog',Get4DaiDogView.as_view(), name="get4daidog"),
    url(r'^api/get5daidog',Get5DaiDogView.as_view(), name="get5daidog"),




    url(r'^api/shanchuqianbao', ShanChuQianBaoView.as_view(), name="shanchuqianbao"),



]