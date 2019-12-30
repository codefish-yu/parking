from django.db import models


from administrator.models import AdminUser as User
from parkinglot.models import ParkingLot 
from company.models import Company
from meta.models import User as CarUser


import datetime


'''计费规则模块'''


class Coupons(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '优惠券'

    type = models.IntegerField(choices=[(0, '打折券'),(1, '代金券'),(2, '抵扣券'),(3, '满时券')])

    name = models.CharField(max_length=200, verbose_name='名称')
    detail = models.CharField(max_length=200, verbose_name='说明')

    rate = models.FloatField(null=True, blank=True, verbose_name='折扣率')
    money = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours = models.FloatField(null=True, blank=True, verbose_name='小时数')

    money1 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours1 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money2 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours2 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money3 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours3 = models.FloatField(null=True, blank=True, verbose_name='小时数')
    money4 = models.FloatField(null=True, blank=True, verbose_name='金额')
    hours4 = models.FloatField(null=True, blank=True, verbose_name='小时数')

    is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    def rule(self):
        if self.type == 0:
            return '计费打 %s 折'% (self.rate/10)
        elif self.type == 1:
            return '计费减免 %s 元' % (self.money)
        elif self.type == 2:
            return '%s 个小时内均计费为 %s 元, 超出部分正常计费' %(self.hours, self.money)
        else:
            s = ''
            if self.money1 and self.hours1:
                s = s + '前 %s 小时计费为 %s 元;'%(self.hours1, self.money1)
            if self.money2 and self.hours2:
                s = s + '\n前 %s 小时计费为 %s 元;'%(self.hours2, self.money2)
            if self.money3 and self.hours3:
                s = s + '\n前 %s 小时计费为 %s 元;'%(self.hours3, self.money3)
            if self.money4 and self.hours4:
                s = s + '\n前 %s 小时计费为 %s 元;'%(self.hours4, self.money4)
            return s


class TicketRecord(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '优惠券出售记录'

    parkinglot = models.ForeignKey(ParkingLot, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    ticket_type = models.IntegerField(choices=[(0, '折扣券'),(1, '代金券'),(2, '抵扣券'),(3, '满时券')])

    coupons = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True)

    buy_time = models.DateTimeField(verbose_name='购买时间',auto_now_add=True,null=True)
    amount = models.IntegerField(null=True, verbose_name='购买上限')
    price = models.FloatField(default=0,verbose_name='单价',null=True)
    extra = models.IntegerField(default=0,verbose_name='余量')

    start_date = models.DateTimeField(null=True, verbose_name='起始日期')
    end_date = models.DateTimeField(null=True, verbose_name='截止日期')

    start_time1 = models.FloatField(null=True, verbose_name='优惠时段起点')
    end_time1 = models.FloatField(null=True, verbose_name='优惠时段截止')

    start_time2 = models.FloatField(null=True, verbose_name='优惠时段起点')
    end_time2 = models.FloatField(null=True, verbose_name='优惠时段截止')
    coucode = models.ImageField(null=True,verbose_name='券码',upload_to='coucode/')
    superpose = models.IntegerField(default=0,verbose_name='是否可叠加',choices=[(0,'否'),(1,'是')])

    # is_delete = models.IntegerField(choices=[(0, '未删除'),(1, '已删除')], default=0)


class CardType(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '月卡类型'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, verbose_name='名称')
    work = models.TextField(max_length=30,null=True,verbose_name='工作开始') 
    relax = models.TextField(max_length=30,null=True,verbose_name='休息开始')
    diff_type = models.IntegerField(null=True,verbose_name='减免指标',choices=[(0,'工作日'),(1,'自定义')],default=0)
    free = models.TextField(max_length=30,null=True,verbose_name='周一优惠开始') 
    free_tu = models.TextField(max_length=30,null=True,verbose_name='周二优惠开始') 
    free_we = models.TextField(max_length=30,null=True,verbose_name='周三优惠开始') 
    free_th = models.TextField(max_length=30,null=True,verbose_name='周四优惠开始') 
    free_fr = models.TextField(max_length=30,null=True,verbose_name='周五优惠开始') 
    free_sa = models.TextField(max_length=30,null=True,verbose_name='周六优惠开始') 
    free_su = models.TextField(max_length=30,null=True,verbose_name='周日优惠开始') 


class Card(models.Model):
    class Meta:
        verbose_name = verbose_name = '月卡'

    status = models.IntegerField(default=0)
    owner = models.CharField(max_length=30,null=True,verbose_name='持卡人')
    car_number = models.CharField(max_length=30,null=True,verbose_name='车牌号')
    phone = models.CharField(max_length=30,verbose_name='联系人电话')
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


#基础规则
class BaseRule(models.Model):
    class Meta:
        verbose_name =verbose_name_plural ='基础规则'

    status = models.IntegerField(default=0)
    parkinglot = models.ForeignKey(ParkingLot,on_delete=models.SET_NULL, null=True)
    per_hour = models.FloatField(default=0,verbose_name='小时费')
    free_time = models.IntegerField(default=0,verbose_name='免费时间')#单位：分钟
    day_max = models.FloatField(default=0,verbose_name='单日最大费用时段')
    min_price = models.IntegerField(default=0,verbose_name='最短计价时间')#单位：分钟
            

class UserCoupon(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户和券'

    user = models.ForeignKey(CarUser, on_delete=models.SET_NULL, null=True, blank=True)
    car_number = models.CharField(max_length=200, null=True, blank=True, verbose_name='车牌')
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    status = models.IntegerField(choices=[(0, '未使用'),(1, '已使用')])

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    use_time = models.DateTimeField(auto_now_add=True, verbose_name='使用时间')













        



