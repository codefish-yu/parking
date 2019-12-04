from django.db import models
from administrator.models import AdminUser as User
from parkinglot.models import ParkingLot 
from company.models import Company
import datetime

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

    # is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)

    def ticket_name(self):
        if self.discount:
            return self.discount.name
        elif self.voucher:
            return self.voucher.name
        elif self.coupon:
            return self.coupon.name
        elif self.hourticket:
            return self.hourticket.name


class CardType(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '月卡类型'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, verbose_name='名称')
    work_start = models.CharField(max_length=30,null=True,verbose_name='工作开始')
    work_end = models.CharField(max_length=30,null=True,verbose_name='工作结束')
    relax_start = models.CharField(max_length=30,null=True,verbose_name='休息开始')
    relax_end = models.CharField(max_length=30,null=True,verbose_name='休息结束')
    diff_type = models.IntegerField(null=True,verbose_name='减免指标',choices=[(0,'工作日'),(1,'单日')],default=0)
    free_start = models.CharField(max_length=30,null=True,verbose_name='周一优惠开始') 
    free_end = models.CharField(max_length=30,null=True,verbose_name='周一优惠结束')
    free_start_tu = models.CharField(max_length=30,null=True,verbose_name='周二优惠开始') 
    free_end_tu = models.CharField(max_length=30,null=True,verbose_name='周二优惠结束')
    free_start_we = models.CharField(max_length=30,null=True,verbose_name='周三优惠开始') 
    free_end_we = models.CharField(max_length=30,null=True,verbose_name='周三优惠结束')
    free_start_th = models.CharField(max_length=30,null=True,verbose_name='周四优惠开始') 
    free_end_th = models.CharField(max_length=30,null=True,verbose_name='周四优惠结束')
    free_start_fr = models.CharField(max_length=30,null=True,verbose_name='周五优惠开始') 
    free_end_fr = models.CharField(max_length=30,null=True,verbose_name='周五优惠结束')
    free_start_sa = models.CharField(max_length=30,null=True,verbose_name='周六优惠开始') 
    free_end_sa = models.CharField(max_length=30,null=True,verbose_name='周六优惠结束')
    free_start_su = models.CharField(max_length=30,null=True,verbose_name='周日优惠开始') 
    free_end_su = models.CharField(max_length=30,null=True,verbose_name='周日优惠结束')
    # is_diff = models.IntegerField(choices=[(0,'否'),(1,'是')],default=0)

 

class Card(models.Model):
    class Meta:
        verbose_name = verbose_name = '月卡'

    status = models.IntegerField(default=0)
    owner = models.CharField(max_length=30,null=True,verbose_name='持卡人')
    car_number = models.CharField(max_length=30,null=True,verbose_name='车牌号')
    phone = models.IntegerField(default=0,verbose_name='联系人电话')
    my_card = models.ForeignKey('CardType',null=True,blank=True, on_delete=models.CASCADE,verbose_name='卡片类型')
    valid_start = models.DateTimeField(null=True , blank=True, verbose_name='有效开始')
    valid_end = models.DateTimeField(null=True , blank=True, verbose_name='有效结束')
    suit = models.ManyToManyField(ParkingLot,verbose_name='所属停车场',related_name='parkinglot_card')

    def get_time(datetime,end):
        if datetime <10:
            datetime = '0'+str(datetime)

        st = str(end.year)+'-'+str(end.month)+'-'+str(end.day) +' '+datetime+':00:00'
        return datetime.datetime.strptime(st,'%Y-%m-%d %H:%M:%S')



    def set_valid_date(self):
        

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

        self.valid_end = get_time(0,end)
        self.save()

    # 普通月卡计费
    def normal_card_cal(self,start,end):

        # 参数：start,end 
        # type:datetime

        # 计算单日需计费小时数
        def nor_one_cal(obj,start,end):
            o_start = obj.valid_start
            o_end = obj.valid_end
            diff2 = start.hour - o_start.hour
            diff3 = end.hour - o_end.hour
            diff4 = end.hour - o_start.hour
            diff5 = start.hour - o_end.hour
            e_mi = end.minute/60
            s_mi = start.minute/60  
            if diff2 < 0 :
                if diff3 >=0:
                    result = - diff2 - diff3 +e_mi - s_mi   
                else:
                    if diff4 < 0:
                        result = end + e_mi - start - s_mi
                    else:
                        result = o_start - start - s_mi
            else:
                if diff5 <0:
                    result = end + e_mi -o_end.hour
                else:
                    result = end + e_mi - start - s_mi
            return result


        diff = end.day-start.day
        diff1 = self.valid_end - self.valid_start 
        price1 = 24-diff1

        if diff > 0:
            results = nor_one_cal(self,start,get_time(23,start)) +(diff-1)*price1 + nor_one_cal(self,get_time(0,end),end)
        else:
            results = nor_one_cal(self,start,end)
        return results

            

















        



