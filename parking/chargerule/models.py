from django.db import models


from administrator.models import AdminUser as User
from parkinglot.models import ParkingLot 
from company.models import Company


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


class TicketRecord(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '优惠券出售记录'

    parkinglot = models.ForeignKey(ParkingLot, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    ticket_type = models.IntegerField(choices=[(0, '折扣券'),(1, '代金券'),(2, '抵扣券'),(3, '满时券')])

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    hourticket = models.ForeignKey(HourTicket, on_delete=models.SET_NULL, null=True)

    buy_time = models.DateTimeField(null=True, verbose_name='购买时间')
    amount = models.IntegerField(null=True, verbose_name='购买数量')

    start_date = models.DateTimeField(null=True, verbose_name='起始日期')
    end_date = models.DateTimeField(null=True, verbose_name='截止日期')

    start_time1 = models.FloatField(null=True, verbose_name='优惠时段起点')
    end_time1 = models.FloatField(null=True, verbose_name='优惠时段截止')

    start_time2 = models.FloatField(null=True, verbose_name='优惠时段起点')
    end_time2 = models.FloatField(null=True, verbose_name='优惠时段截止')


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
    my_card = models.ForeignKey('CardType',null=True,blank=True, on_delete=models.CASCADE,verbose_name='卡片类型')
    valid_start = models.DateTimeField(null=True , blank=True, verbose_name='有效开始')
    valid_end = models.DateTimeField(null=True , blank=True, verbose_name='有效结束')
    work_start = models.CharField(max_length=30,null=True,verbose_name='工作开始')
    work_start = models.CharField(max_length=30,null=True,verbose_name='工作结束')
    workdays = models.TextField(null=True , blank=True, verbose_name='工作日')
    holidays = models.TextField(null=True , blank=True, verbose_name='节假日')


    def set_valid_date(self):
        import datetime

        self.valid_start =now
        now = datetime.datetime.now()
        end = now
        diff = end.month - now.month
        if now.day == 1:
            
            while  diff == 0:
                end += datetime.timedelta(days=1)
        else:
            while  diff < 2:
                end += datetime.timedelta(days=1)
        str = datetime.date.strftime(now,"%Y %m %H:%M:%S")
        # end = end - datetime.timedelta(days=1)
        st = str(end.year)+'-'+str(end.month)+'-'+str(end.day) +' '+'00:00:00'
        self.valid_end = datetime.datetime.strptime(st,'%Y-%m-%d %H:%M:%S')






        



