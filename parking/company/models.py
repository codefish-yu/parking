from django.db import models

# Create your models here.


'''合作商户模块'''

class Company(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商户管理'

	status = models.IntegerField(default=0,verbose_name='状态',choices=[(0,'冻结'),(1,'激活')])
	name = models.CharField(max_length=30, verbose_name='商家名称')
	account = models.CharField(max_length=30,unique=True,verbose_name='登录账号')
	owner = models.CharField(max_length=30,verbose_name='联系人姓名')
	phone = models.IntegerField(default=0,verbose_name='联系人电话')
	balance = models.FloatField(default=0,verbose_name='余额')
	duration = models.FloatField(default=0,verbose_name='时长')
	type = models.IntegerField(default=0,verbose_name='限制类型',choices=[(0,'无限制'),(1,'限制天'),(2,'限制周'),(3,'限制月')])
	rule = models.CharField(max_length=100,null=True,verbose_name='限制规则')
	amount = models.IntegerField(default=0,verbose_name='限制张数')
	descript = models.CharField(max_length=100,verbose_name='商家描述',null=True)



		