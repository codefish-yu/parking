from django.db import models
from chargerule.models import Coupons,TicketRecord
from company.models import Company
from meta.models import User,Product

# Create your models here.


class ApplyRecord(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '申请记录'

	# keyword:名称，类型，数量，商家，时间
	coupon = models.ForeignKey(TicketRecord,verbose_name='券',on_delete=models.SET_NULL,null=True)
	number = models.IntegerField(default=0,verbose_name='数量')
	time = models.DateTimeField(auto_now_add=True,verbose_name='申请时间',null=True)
	status = models.IntegerField(default=1,verbose_name="状态",choices = [(0,'审核中'),(1,'使用中'),(2,'未通过')])
	bill = models.ForeignKey('BusinessBill',verbose_name='商户账单',on_delete=models.SET_NULL,null=True)


class BusinessBill(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商户账单'

	status= models.IntegerField(default=0,verbose_name='支付状态',choices=[(0,'待支付'),(1,'已支付')])
	cost = models.FloatField(default=0,verbose_name='费用')
	create_time = models.DateTimeField(auto_now_add=True,null=True)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL,blank=True)


# class Ticket(models.Model):
# 	class Meta:
# 		verbose_name='用户领券记录'

# 	coupon = models.ForeignKey(TicketRecord,verbose_name='券',on_delete=models.SET_NULL,null=True)
# 	amount = 



