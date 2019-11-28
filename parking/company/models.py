from django.db import models
from administrator.models import AdminUser as User

# Create your models here.


'''合作商户模块'''

class Company(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商户管理'

	status = models.IntegerField(default=0,verbose_name='状态',choices=[(-1,'删除'),(0,'冻结'),(1,'激活')])
	name = models.CharField(max_length=30, null=True,verbose_name='商家名称')
	address = models.CharField(max_length=30,null=True,verbose_name='商家地址')
	account = models.CharField(max_length=30,verbose_name='登录账号')
	owner = models.CharField(max_length=30,verbose_name='联系人姓名')
	phone = models.IntegerField(default=0,verbose_name='联系人电话')
	balance = models.FloatField(default=0,verbose_name='余额')
	duration = models.FloatField(default=0,verbose_name='时长')
	type = models.IntegerField(default=0,verbose_name='限制类型',choices=[(0,'无限制'),(1,'限制天'),(2,'限制周'),(3,'限制月')])
	rule = models.CharField(max_length=100,null=True,verbose_name='限制规则')
	amount = models.IntegerField(default=0,verbose_name='限制张数')
	descript = models.CharField(max_length=100,verbose_name='商家描述',null=True)


class Refund(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '退款记录'

	company = models.ForeignKey('Company',null=True,on_delete=models.CASCADE)
	money = models.FloatField(default=0,verbose_name='退款金额')
	duration = models.FloatField(default=0,verbose_name='退款时长')
	cost = models.FloatField(default=0,verbose_name='退还费用')
	reason = models.CharField(max_length=100,verbose_name='退款原因')
	create_time = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=0,verbose_name='状态',choices=[(-1,'删除'),(0,'未审核'),(1,'已审核')])


class  Recharge(object):
	class Meta:
		verbose_name = verbose_name_plural = '充值记录'

	type = models.ForeignKey('Ticket',null=True,on_delete=models.CASCADE)#代金，折扣，满时
	denomination = models.FloatField(default=0,verbose_name='面额')
	amount = models.IntegerField(default=0,verbose_name='张数')
	valid_start = models.CharField(max_length=30,null=True,verbose_name='有效开始')
	valid_end = models.CharField(max_length=30,null=True,verbose_name='有效结束')
	status = models.IntegerField(default=0,verbose_name='状态',choices=[(-1,'删除'),(0,'未审核'),(1,'已审核')])
	create_time = models.DateTimeField(auto_now_add=True)


class NormalCard(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '普通月卡'

	status = models.IntegerField(default=0)
	valid_start = CharField(max_length=30,null=True,verbose_name='有效开始')
	valid_end = models.CharField(max_length=30,null=True,verbose_name='有效结束')
	holidays = models.TextField(null=True , blank=True, verbose_name='非工作日')

class RerveseCard(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '错峰卡'

	status = models.IntegerField(default=0)
	valid_start = CharField(max_length=30,null=True,verbose_name='有效开始')
	valid_end = models.CharField(max_length=30,null=True,verbose_name='有效结束')
	valid_start1 = CharField(max_length=30,null=True,verbose_name='有效开始')
	valid_end1 = models.CharField(max_length=30,null=True,verbose_name='有效结束')
	holidays = models.TextField(null=True , blank=True, verbose_name='非工作日')


class UserCard(models.Model):
	class Meta:
		verbose_name = verbose_name = '商家普通月卡'

	status = models.IntegerField(default=0)
	user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	normalcard = models.ForeignKey('NormalCard',null=True,blank=True, on_delete=models.CASCADE)
	normalcard = models.ForeignKey('RerveseCard',null=True,blank=True,on_delete=models.CASCADE)






		


		








	
			
		



		