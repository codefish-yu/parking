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
def chec_days(start,end,obj,card):
    diff = get_day(start,end)
    if card.my_card.diff_type == 0:
        if diff == 0:
            result = chec_work(start,end,card,obj.parkinglot)
        else:
            result = chec_work(start,24.0,card,obj.parkinglot) + (diff-1)*chec_work(0.0,24.0,card,obj.parkinglot)+chec_work(0.0,end,card,obj.parkinglot)
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




    

    



  
