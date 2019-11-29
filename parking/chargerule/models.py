from django.db import models
from administrator.models import AdminUser as User
from parkinglot.models import ParkingLot 

# Create your models here.



'''计费规则模块'''


class Discount(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '打折券'

    rate = models.FloatField(null=True, blank=True, verbose_name='折扣率')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
    rule = models.CharField(max_length=200, verbose_name='细则')

    is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class Voucher(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '代金券'

    money = models.FloatField(null=True, blank=True, verbose_name='金额')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
    rule = models.CharField(max_length=200, verbose_name='细则')
    
    is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class Coupon(models.Model):
    class Meta: 
        verbose_name = verbose_name_plural = '抵扣券'
        '''规定小时内只付一定的钱, 超出时间算临停'''

    money = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours = models.FloatField(null=True, blank=True, verbose_name='小时数')
    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='备注')
    rule = models.CharField(max_length=200, verbose_name='细则')
    
    is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


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
    rule = models.CharField(max_length=200, verbose_name='细则')
    
    is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class CardType(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '月卡类型'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, verbose_name='名称')
    rule = models.CharField(max_length=100,verbose_name='描述',null=True)
    suit = models.duoshipin = models.ManyToManyField(ParkingLot, verbose_name='可用停车场')
 

class Card(models.Model):
    class Meta:
        verbose_name = verbose_name = '月卡'

    status = models.IntegerField(default=0)
    owner = models.ForeignKey(User,null=True,on_delete=models.CASCADE,verbose_name='持卡人')
    my_card = models.ForeignKey('Card',null=True,blank=True, on_delete=models.CASCADE,verbose_name='卡片类型')
    valid_start = models.DateTimeField(null=True , blank=True, verbose_name='有效开始')
    valid_end = models.DateTimeField(null=True , blank=True, verbose_name='有效结束')
    holidays = models.TextField(null=True , blank=True, verbose_name='非工作日')



