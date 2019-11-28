from django.db import models
from administrator.models import AdminUser as User

# Create your models here.



'''计费规则模块'''


class Discount(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '打折券'

    rate = models.FloatField(null=True, blank=True, verbose_name='折扣率')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
 

class Voucher(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '代金券'

    money = models.FloatField(null=True, blank=True, verbose_name='金额')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
    

class Coupon(models.Model):
    class Meta: 
        verbose_name = verbose_name_plural = '抵扣券'
        '''规定小时内只付一定的钱, 超出时间算临停'''

    money = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours = models.FloatField(null=True, blank=True, verbose_name='小时数')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
 

class HourTicket(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '满时券'

    money1 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours1 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money2 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours2 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money3 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours3 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money4 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours4 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
 

class NormalCard(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '普通月卡'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, verbose_name='名称')
    valid_start = models.CharField(max_length=30,null=True,verbose_name='有效开始')
    valid_end = models.CharField(max_length=30,null=True,verbose_name='有效结束')
    holidays = models.TextField(null=True , blank=True, verbose_name='非工作日')

class RerveseCard(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '错峰卡'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, verbose_name='名称')
    valid_start =models.CharField(max_length=30,null=True,verbose_name='有效开始')
    valid_end = models.CharField(max_length=30,null=True,verbose_name='有效结束')
    valid_start1 = models.CharField(max_length=30,null=True,verbose_name='有效开始')
    valid_end1 = models.CharField(max_length=30,null=True,verbose_name='有效结束')
    holidays = models.TextField(null=True , blank=True, verbose_name='非工作日')


class UserCard(models.Model):
    class Meta:
        verbose_name = verbose_name = '商家普通月卡'

    status = models.IntegerField(default=0)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    normalcard = models.ForeignKey('NormalCard',null=True,blank=True, on_delete=models.CASCADE)
    normalcard = models.ForeignKey('RerveseCard',null=True,blank=True,on_delete=models.CASCADE)