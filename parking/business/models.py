from django.db import models
from chargerule.models import Coupons
from company.models import Company
from meta.models import User

# Create your models here.


class ApplyRecord(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '申请记录'

	# keyword:名称，类型，数量，商家，时间
	coupon = models.ForeignKey(Coupons,verbose_name='券',on_delete=models.SET_NULL,null=True)
	number = models.IntegerField(default=0,verbose_name='数量')
	company = models.ForeignKey(Company,verbose_name='商家',on_delete=models.SET_NULL,null=True)
	time = models.DateTimeField(auto_now_add=True,verbose_name='申请时间')
	status = models.IntegerField(default=0,verbose_name="状态",choices = [(0,'待审核'),(1,'使用中'),(2,'审核失败')])


class BusinessBill(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商户账单'




