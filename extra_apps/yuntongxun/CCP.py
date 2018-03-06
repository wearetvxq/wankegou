# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708605841b501605988b01e0158';

# 主帐号Token
accountToken = '6c11af16db4947a69c052a007bbfea1b';

# 应用Id
appId = '8a216da8612b461d01612bb8c8b2006d';

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';

#
class _CCP(object):
    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)


ccp = _CCP.instance()

#
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


if __name__ == '__main__':
    ccp.sendTemplateSMS('18064129048', ['122134', 5], 232401)
    # sendTemplateSMS('18696100212', '122134', 1)
# 短信模板查询
# @param templateId  必选参数   模板Id，不带此参数查询全部可用模板
# def QuerySMSTemplaterySMSTemplate(templateId):
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)

# result = rest.QuerySMSTemplate(templateId)
# i=1
# for k,v in result.iteritems():
#
#     if k=='TemplateSMS' :
#         for m in v:
#             print ('第'+str(i)+'个模板')
#             i=i+1
#             for k,v in m.iteritems():
#                 print '%s:%s' % (k, v)
#     else:
#         print '%s:%s' % (k, v)
#

# QuerySMSTemplate('')