from .models import *
from chargerule.models import *
from parkinglot.models import Calendar


import re
import math
import json
import datetime
import calendar


# 以下为计费模块


# get_hours获取一段时间的小时数, 返回类型为小数
def get_hours(start, end):
    diff = end - start
    days = diff.days
    seconds = diff.seconds
    
    return days + seconds / 3600


# get_if_work获取今天是否是工作日
def get_if_work(day, parkinglot):
    ifwork = True  # 判断是否工作日
    weekday = day.weekday()

    if Calendar.objects.filter(parkinglot=parkinglot, day=day).exists():
        ifwork = Calendar.objects.filter(parkinglot=parkinglot, day=day).first().ifwork
    
    elif Calendar.objects.filter(day=day).exists():
        ifwork = Calendar.objects.filter(day=day).first().ifwork
    
    else:
        ifwork = True if weekday < 5 else False

    return ifwork


# str_2_float'08:30' 转成 8.5
def str_2_float(hour): 
    a = hour.split(':')
    return int(a[0]) + int(a[1]) / 60


# date_2_float日期中的时间转成小数
def date_2_float(e):
    s = datetime.datetime(e.year, e.month, e.day, 0, 0, 0)
    return get_hours(s, e)


# get_valid_hours根据国家规定的封顶时间,计算有效计费时长
def get_valid_hours(start, end, day_max=8):
    if start <= end:
        diff = end - start
        days = diff.days
        seconds = diff.seconds

        hours = days * day_max + (seconds/3600 if seconds/3600 <= day_max else day_max)

        return hours
        
    return 0


# get_valid_hours_perday获取在自然日内的错峰时长
def get_valid_hours_perday(areas, start=None, end=None):
    hours = 0
    if start and end: # 同一天
        hours = date_2_float(end) - date_2_float(start)
        end = date_2_float(end)
        start = date_2_float(start)
        for i in areas:
            s = str_2_float(i['start'])
            e = str_2_float(i['end'])
            if start < s and end > e:
                hours -= e - s
                print(1)
            elif start <= s and end >= s:
                print(2)
                hours -= end - s
            elif start <= e and end >= e:
                print(3)
                hours -= e - start
            elif start >= s and end <= e:
                print(4)
                hours = 0
                break
            print(start,end,i,s,e, hours)

    elif start:
        clock = date_2_float(start)
        hours = 24 - clock
        for i in areas:
            s = str_2_float(i['start'])
            e = str_2_float(i['end'])

            if s > clock:
                hours = hours - (e -s)
            elif e > clock:
                hours = hours - (e - clock)

    else:
        hours = date_2_float(end)
        clock = hours
        for i in areas:
            s = str_2_float(i['start'])
            e = str_2_float(i['end'])

            if e < clock:
                hours = hours - (e -s)
            elif s < clock:
                hours = hours - (clock -s)
    print('获取在自然日内的错峰时长:', areas, start, end, hours)
    return hours if hours > 0 else 0


# get_valid_hours_per24 计算每一个非自然日的有效时长
def get_valid_hours_per24(start, end, parkinglot, card):
    
    def getareas1(ifwork, card):
        work = json.loads(card.work.replace('\'','\"')) if card.work else []
        relax = json.loads(card.relax.replace('\'','\"')) if card.relax else []
        return work if ifwork else relax
    def getareas2(week_day, card): # 获取时段 如: [{"start": "22:00", "end": "24:00"}]
        if week_day == 0:
            areas = card.free
        if week_day == 1:
            areas = card.free_tu
        if week_day == 2:
            areas = card.free_we
        if week_day == 3:
            areas = card.free_th
        if week_day == 4:
            areas = card.free_fr
        if week_day == 5:
            areas = card.free_sa
        if week_day == 6:
            areas = card.free_su 
        return json.loads(areas.replace('\'', '\"')) if areas else []

    hours = 0

    start_day = start.date()
    end_day = end.date()
     
    start_weekday = start_day.weekday()
    end_weekday = end_day.weekday()
    ifwork1 = get_if_work(start_day, parkinglot)
    ifwork2 = get_if_work(end_day, parkinglot)
    
    if card.diff_type == 0:
        areas1 = getareas1(ifwork1, card)
        areas2 = getareas1(ifwork2, card)
    else:
        areas1 = getareas2(start_weekday, card)
        areas2 = getareas2(end_weekday, card)

    if start_day == end_day:
        return get_valid_hours_perday(areas1, start, end)
    else:
        hours1 = get_valid_hours_perday(areas1, start=start)
        hours2 = get_valid_hours_perday(areas2, end=end)
        return hours1 + hours2


# 获取错峰卡后的计费时长
def get_by_card(start, end, parkinglot, card, day_max):
    
    days = (end - start).days
  
    hours = 0
    for i in range(days+1):
        _end = start + datetime.timedelta(days=1)
        if _end > end:
            h = get_valid_hours_per24(start, end, parkinglot, card)
            hours += h if h < day_max else day_max
            break
        else:
            h = get_valid_hours_per24(start, _end, parkinglot, card)
           
            hours += h if h < day_max else day_max
            start = _end
    return hours


def hours2price(hours, baseRule):
    '''返回费用, 和可滞留时间'''
    basehour = baseRule.free_time / 60
    minhour = baseRule.min_price / 60
    if hours <= basehour:
        return 0, basehour - hours
    if hours <= minhour:
        return baseRule.per_hour * minhour, minhour - hours + basehour
    
    valid_hour = math.ceil(hours * 2) / 2
    return valid_hour * baseRule.per_hour, valid_hour - hours + basehour


'''
计算费用, 有卡则用卡不能用券, 用券时可叠加同种券, 不能叠加不同种类的券
@author dusc
@param baseRule 基本收费规则对象, start 开始计费时间, end 停止计费时间, coupons 优惠券对象, card 会员卡
'''
def compute(parkinglot, start, end, coupons, card):
    if end <= start:
        return 0,0,datetime.datetime.now()

    baseRule = BaseRule.objects.filter(parkinglot=parkinglot, status=0).first()
    day_max = baseRule.day_max
    per_hour = baseRule.per_hour
    free_time = baseRule.free_time
    min_price = baseRule.min_price

    if card: # 有卡
        hours = 0

        if start >= card.valid_end or end <= card.valid_start:
            hours = get_valid_hours(start, end)
        elif start < card.valid_start and end < card.valid_end:
            hours = get_by_card(card.valid_start, end, parkinglot, card.my_card, day_max) + get_valid_hours(start, card.valid_start, day_max)
        elif start > card.valid_start and end > card.valid_end:
            hours = get_by_card(start, card.valid_end, parkinglot, card.my_card, day_max) + get_valid_hours(card.valid_end, end, day_max)
        else:
            hours = get_by_card(start, end, parkinglot, card.my_card, day_max)
            print('hours', hours)
        if hours == get_valid_hours(start, end):     # 说明错峰卡没有生效, 停车时间跟错峰时间没有重叠
            payment, left_time = hours2price(hours, baseRule) 
            latest_leave_time = end + datetime.timedelta(hours=left_time)      # 超过这个时间, 就会产生滞留费
            payable = payment

        else:                                        # 错峰卡生效, 超出的时间按每半小时一计
            payable = payment = math.ceil(hours * 2) / 2 * baseRule.per_hour
            left_time = math.ceil(hours * 2) / 2 - hours + free_time/60
            print('left_time', hours, left_time)
            latest_leave_time = end + datetime.timedelta(hours=left_time)

    else:
        hours = get_valid_hours(start, end, day_max)

        payment, left_time = hours2price(hours,baseRule)
        latest_leave_time = end + datetime.timedelta(hours=left_time)      # 超过这个时间, 就会产生滞留费
        payable = payment

        if coupons: # 有券, 只能同时用一种券, 可叠加多张
            for coupon in coupons:
                if coupon.type == 0:
                    payment = payment * coupon.rate / 100

                elif coupon.type == 1:
                    payment = payment - coupon.money

                elif coupon.type == 2: 
                    if hours > 0:
                        if hours <= coupon.hours:
                            payment = coupon.money
                            hours = 0
                        else:
                            hours = hours - coupon.hours
                            payment = payment - coupon.hours * per_hour + coupon.money

                elif coupon.type == 3:
                    if coupon.hours4 and coupon.hours4 <= hours:
                        payment = payment - coupon.hours4 * per_hour + coupon.money4
                        hours -= coupon.hours4
                    elif coupon.hours3 and coupon.hours3 <= hours:
                        payment = payment - coupon.hours3 * per_hour + coupon.money3
                        hours -= coupon.hours3
                    elif coupon.hours2 and coupon.hours2 <= hours:
                        payment = payment - coupon.hours2 * per_hour + coupon.money2
                        hours -= coupon.hours2
                    elif coupon.hours1 and coupon.hours1 <= hours:
                        payment = payment - coupon.hours1 * per_hour + coupon.money1
                        hours -= coupon.hours1

    return payable, payment, latest_leave_time 
        

# 计价
def charge(in_and_out, coupons=None):
    card = in_and_out.parkinglot.parkinglot_card.filter(car_number=in_and_out.number).first()
    return compute(in_and_out.parkinglot, in_and_out.in_time, in_and_out.out_time, coupons, card)



def compute_demurrage(parkinglot, out_time, latest_leave_time, card, final_out_time=None):
    print('ssssss',out_time, latest_leave_time, final_out_time)
    if not final_out_time:
        final_out_time = datetime.datetime.now()
     
    if final_out_time < latest_leave_time:
        return 0
    else:
         
        baseRule = BaseRule.objects.filter(parkinglot=parkinglot, status=0).first()
        day_max = baseRule.day_max
        per_hour = baseRule.per_hour
        free_time = baseRule.free_time
        min_price = baseRule.min_price


        start = latest_leave_time - datetime.timedelta(hours=free_time/60)
        end = final_out_time

        left_time = get_hours(out_time, start) # 计算停车费时,计费时间减去实际停车时间, 比如停车2.1小时,算成2.5小时的钱, 那么就多算了0.4小时, 这是可以用作滞留时间的
        if end <= start:
            return 0

        if card: # 有卡
            hours = 0

            if start > card.valid_end or end < card.valid_start:
                hours = get_valid_hours(start, end)
            elif start < card.valid_start and end < card.valid_end:
                hours = get_by_card(card.valid_start, end, parkinglot, card.my_card, day_max) + get_valid_hours(start, card.valid_start, day_max)
            elif start > card.valid_start and end > card.valid_end:
                hours = get_by_card(start, card.valid_end, parkinglot, card.my_card, day_max) + get_valid_hours(card.valid_end, end, day_max)
            else:
                hours = get_by_card(start, end, parkinglot, card.my_card, day_max)
                print(hours, left_time)
                if hours <= left_time + free_time/60:
                    hours = 0
                else:
                    hours = hours - left_time
                print('hours', hours)
        else:
            hours = get_valid_hours(start, end, day_max)
        
        valid_hour = math.ceil(hours * 2) / 2
        
        return valid_hour * per_hour


# 计算滞留费
def demurrage(in_and_out):
    card = in_and_out.parkinglot.parkinglot_card.filter(car_number=in_and_out.number).first()
    parkinglot = in_and_out.parkinglot
    out_time = in_and_out.out_time
    latest_leave_time = in_and_out.latest_leave_time

    return charge_demurrage(parkinglot, out_time, latest_leave_time, card)
    