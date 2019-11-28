from django.db import models

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
 
