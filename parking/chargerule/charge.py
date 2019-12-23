from .models import *
from chargerule.models import *
from parkinglot.models import Calendar


import re
import math
import json
import datetime
import calendar


# 以下为计费模块


# time to float
def transform(st):
    if st and str(type(st)) != "<class 'float'>":
        if st.replace(':30','.5') == st:

            return float(st.replace(':00','.0'))
        else:
            return float(st.replace(':30','.5'))

    return st


# 转json
def to_dobule(str):
    t = json.loads(str.replace("'",'"')) if str else ''
    for i in t:
        i['start'] = transform(i['start'])
        i['end'] = transform(i['end'])
    return t


# 根据日自定义datetime
def get_time(datetime,end):
        if datetime <10:
            datetime = '0'+str(datetime)

        st = str(end.year)+'-'+str(end.month)+'-'+str(end.day) +' '+datetime+':00:00'
        return datetime.datetime.strptime(st,'%Y-%m-%d %H:%M:%S')


def get_year(year):
    sum = 0
    for i in range(1,13):
        sum += calendar.monthrange(year,i)[1]
    return sum


def get_month_and_extra(start,end):
    sum = 0
    for i in range(start.month+1,end.month):
        sum += calendar.monthrange(start.year,i)[1]

    return sum +calendar.monthrange(start.year,start.month)[1]-start.day+end.day-1


def get_day(start,end):
    year_diff = end.year - start.year
    month_diff = end.month - start.month
    day_diff = end.day - start.day
    if year_diff ==0:
        if month_diff == 0:
            return day_diff
        else:
            return get_month_and_extra(get_month_and_extra)
    else:
        diff1 = 12-start.month 
        diff2 = end.month-1
        d1 = calendar.monthrange(start.year,start.month)[1] - start.day
        d2 = end.day -1
        if diff1 != 0:
            for i in range(start.month+1,13):
                d1 += calendar.monthrange(start.year,i)[1]
        if diff2 !=0:
            for i in range(1,end.month):
                d2 += calendar.monthrange(end.year,i)[1]
        y = d1 + d2
        for i in range(start.year+1,year_diff):
            y += get_year(i)
        return y


def time_float(t):
    if isinstance(t,float):
        return t
    else:
        return t.hour + t.minute/60

# 获取单段时间重合
def get_repeat(s,e,l):
    if s <l['start']:
        if e < l['start']:
            return 0
        elif e >=l['start'] and e <=l['end']:
            return e - l['start']
        else:
            return l['end'] - l['start']
    elif s >=l['start'] and s <=l['end']:
        if e <=l['end']:
            return e-s
        else:
            return l['end'] - s
    else:
        return 0


# 价格计算
def cal(tmp,parkinglot):
    rule = BaseRule.objects.filter(parkinglot=parkinglot).first()
    free = rule.free_time/60
    c = tmp-free
    mx = rule.day_max
    mi = rule.min_price/60
    ho = rule.per_hour
    if c<= 0 :
        return 0
    elif c >0 and c <= mi:
        return mi/ho
    elif c > mi and c <=mx:
        if c%1 <=mi:
            return (c-c%1 +mi)*ho
        else:
            if math.ceil(c%1/mi ) >=(ho/mi):
                return (c-c%1 +1)*ho
            else:
                return (c-c%1+math.ceil(c%1/mi )*mi)*ho
    else:
        return 8*ho


# 无卡计算
def no_card(start,end,parkinglot):
    diff = get_day(start,end)
    start = time_float(start)
    end = time_float(end)
    if diff == 0:
        return cal(end-start,parkinglot)
    else:
        result = cal(24-start,parkinglot)+cal(end-0,parkinglot)+(diff-1)*cal(24,parkinglot)
        return result
        
# 单日计算
def cal_one_day(start,end,time_list,parkinglot):
    start = time_float(start)
    end = time_float(end)
    li = to_dobule(time_list)
    tmp = end -start
    for i in li:
        tmp-=get_repeat(start,end,i)
    return cal(tmp,parkinglot)
    

# 判断工作日   
def chec_work(start,end,card,parkinglot):
    # 后需增加判断工作日的逻辑
    workday =True
    if workday:
        return cal_one_day(start,end,card.my_card.work,parkinglot)
    else:
        return cal_one_day(start,end,card.my_card.relax,parkinglot)


# 判断周几
def chec_weekday(start,end,card,parkinglot,d):

    if d == 1:
        return cal_one_day(start,end,card.my_card.free,parkinglot)
    elif d ==2:
        return cal_one_day(start,end,card.my_card.free_tu,parkinglot)
    elif d ==3:
        return cal_one_day(start,end,card.my_card.free_we,parkinglot)
    elif d ==4:
        return cal_one_day(start,end,card.my_card.free_th,parkinglot)
    elif d == 5:
        return cal_one_day(start,end,card.my_card.free_fr,parkinglot)
    elif d == 6:
        return cal_one_day(start,end,card.my_card.free_sa,parkinglot)
    elif d == 7:
        return cal_one_day(start,end,card.my_card.free_su,parkinglot)


# 判断多日
def chec_days(start,end,parkinglot,card):
    diff = get_day(start,end)
    if card.my_card.diff_type == 0:
        if diff == 0:
            result = chec_work(start,end,card,parkinglot)
        else:
            result = chec_work(start,24.0,card,parkinglot) + (diff-1)*chec_work(0.0,24.0,card,parkinglot)+chec_work(0.0,end,card,parkinglot)
    else:
        if diff == 0:
            result = chec_weekday(start,end,card,parkinglot,start.weekday())
        else:
            tip = start.weekday()+1
            result1 = chec_weekday(start,end,card,parkinglot,tip) + chec_weekday(start,end,card,parkinglot,end.weekday()+1)
            for i in range(tip+1,tip+diff):
                t = i%7
                if t == 0:
                    t = 7
                chec_weekday(0.0,24.0,card,parkinglot,t)

    return result



# 根据出入场记录计算费用
# get_price函数传入的对象必需包含以下参数：停车场、入场时间、出场时间、根据是否有卡，计费方式产生差异
def get_price(obj):
    start = obj.in_time
    end = obj.out_time
    card = Card.objects.filter(car_number=obj.number).first()
    if card:
        now = datetime.datetime.now()
        if obj.parkinglot not in card.suit.all():

            return no_card(start,end,obj.parkinglot)
        elif card.valid_end < now:
            if start <card.valid_end and card.valid_end <end:

                result = chec_days(start,card.valid_end,obj,card)+no_card(get_time(24,card.valid_end),end,obj.parkinglot)
                return  result
            else:
                return no_card(start,end,obj.parkinglot)

            
        else:
            return chec_days(start,end,obj,card)

    else:
        return no_card(start,end,obj.parkinglot)


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
        print(start, end)
        hours = date_2_float(end) - date_2_float(start)
        end = date_2_float(end)
        start = date_2_float(start)
        print('sss',start, end, hours)
        for i in areas:
            s = str_2_float(i['start'])
            e = str_2_float(i['end'])
            if start < s and end > e:
                hours -= e - s
                print(1)
            elif start <= s and end >= s:
                print(2)
                hours -= e - s
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
        print(areas)
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
            print('sssxxx',start, end, h)
            hours += h if h < day_max else day_max
            break
        else:
            h = get_valid_hours_per24(start, _end, parkinglot, card)
            print('xxxxxxxx',start, _end, h)
           
            hours += h if h < day_max else day_max
            start = _end
    return hours


def hours2price(hours, baseRule):
    if hours <= baseRule.free_time / 60:
        return 0
    if hours <= baseRule.min_price / 60:
        return baseRule.per_hour * baseRule.min_price / 60
     
    return math.ceil(hours * 2) / 2 * baseRule.per_hour


'''
计算费用, 有卡则用卡不能用券, 用券时可叠加同种券, 不能叠加不同种类的券
@author dusc
@param baseRule 基本收费规则对象, start 开始计费时间, end 停止计费时间, coupons 优惠券对象, card 会员卡
'''
def compute(parkinglot, start, end, coupons, card):

    baseRule = BaseRule.objects.filter(parkinglot=parkinglot).first()
    day_max = baseRule.day_max
    per_hour = baseRule.per_hour
    free_time = baseRule.free_time
    min_price = baseRule.min_price

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
        print(hours , 'xxxx')
        
        payable = payment = math.ceil(hours * 2) / 2 * baseRule.per_hour

    else:
        hours = get_valid_hours(start, end, day_max)

        payable = payment = hours2price(hours,baseRule)
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

    return payable, payment 
        
# 计价
def charge(in_and_out, coupons):
    card = Card.objects.filter(car_number=in_and_out.number)
    compute(in_and_out.parkinglot, in_and_out.in_time, in_and_out.out_time, coupons, card)


  

    

    



  
