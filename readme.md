逻辑
验证userid当狗不属于你 且 正常 只能看到 掘金等东西
当狗不属于你 且 出售 能看到购买
当狗不属于你 且 生殖 能看到生殖

属于你
都有
一个状态

购买 自己 宠物 提前验证
user 的数据 狗狗数量 等
买的话 type 1 mydogid -1
生 type 2 mydogid = 父亲id

try:
weishijilu.save()
except Exception as e:
log.error(e)

       奖池用户不能有狗
			 
 掘金和 加入1要看喂食hash2首页看到狗的属性3输入密码太多4出售 喂食需要删除0.00喂空 0.5doginfo 体重改成长奖池交易记录 手续费给到我的 余额生限制 卖限制 后台id购买和生育的

主体功能全部完成
美工：界面宣传 新的狗图片
数据公式：具体掘金 生殖后代属性 生殖周期 喂养暴击 等数据相关
待完善功能 ：锁单，交易记录，抽奖
新功能：元气 待开发  


重点
js
![image](https://user-images.githubusercontent.com/32411303/124714260-1d6e6680-df34-11eb-9423-3719e35f88a3.png)
html
</div>
<div class="user-info fr"><span><i class="fa fa-user fa-lg"></i></span> <a class="user-name" href="/my.html"></a></div>
</div>

py



class CheckLoginHandler(BaseHandler):
"""检查登陆状态"""
def get(self):
# get_current_user方法在基类中已实现，它的返回值是session.data（用户保存在redis中
# 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
if self.get_current_user():
self.write({"errcode":RET.OK, "errmsg":"true", "data":{"name":self.session.data.get("name")}})
else:
self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})

return HttpResponseRedirect(reverse(url))问题Reverse for 'user/api/jh3' with arguments '()' and keyword arguments '{}' not found. 0 pattern(s) tried: []

red = HttpResponseRedirect("user/jihuo")
return red
失败 这是追加url

验证码
验证手机号
验证码时间

users模型类
手机号
密码
名称
钱包地址

是否激活
激活金额
余额
冻结金额

market
houzi模型
所属用户
成长
生育
掘金
掘金表
喂食表

home
用户操作
![image](https://user-images.githubusercontent.com/32411303/124714321-34ad5400-df34-11eb-9866-391405220405.png)

交易记录模型
所属用户
交易类型
交易时间
交易金额
