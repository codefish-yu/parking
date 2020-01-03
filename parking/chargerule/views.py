from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from company.models import Company
from parkinglot.models import ParkingLot
from administrator.models import AdminUser 
from business.views import ran
from administrator.decorators import page, _save_attr_,export_excel
import io


'''计费规则管理'''

@page
def base_rule(request):
    '''基本计费规则配置'''
    ctx = {}
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':

            r = BaseRule()
            _save_attr_(r, request)
            park = request.POST.get('parkinglot')
            if park:
                r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
                r.save()

        elif action == 'update':
            id = request.POST.get('id', '')
            r = BaseRule.objects.filter(id=id).first()
            _save_attr_(r, request)
            park = request.POST.get('parkinglot')
            if park:
                r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
                r.save()

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = BaseRule.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()


    ctx['parkinglots'] = ParkingLot.objects.all()
    ctx['rules'] =ctx['objects'] = BaseRule.objects.filter(status=0).all() 
    return (ctx,'base_rule.html')


@page
def card_type(request):
    '''卡片类型设置'''
    import json

    def chec(str):
        if str.replace('.5',':30') == str:
            return str+':00'
        else:
            return '2'
   
    def tim():
        def rm_invalid(t):
            if t%1 == 0:
                return int(t)
            return t
        list = []
        list1 = []
        for i in range(24):
            k = rm_invalid((i)/2)
            k1 = rm_invalid((i+24)/2)
            c = {
            'k':k,
            'v':chec(str(k))
            }
            c1 = {
            'k':k1,
            'v':chec(str(k1))
            }

            list.append(c)
            list1.append(c1)

        return list,list1

    def cut_time(time):
        tim_list = []
        guide = []
        start = 0
        for i,j in enumerate(time):
            # print(i)
            if j == ',':
                tip =False
                tim_list.append(time[start:i])
                start = i+1

        tim_list.append(time[start:])

        return get_start_and_end(tim_list)


    def get_start_and_end(list):

        def get(time):
            for i,j in enumerate(time):
                if j == '-':
                    return time[0:i],time[i+2:]


        tmp = []
        for m in list:
            start,end = get(m)
            c = {
                    "start":start,
                    "end":end
                }
            tmp.append(c)
        return tmp


    def save_time(obj,request):
        fields = obj._meta.fields
        
        for field in fields:
            field_name = field.name
            if str(type(field)) == "<class 'django.db.models.fields.TextField'>":
                value = request.POST.get(field_name, '')
                if value.strip() != '':
                    obj.__setattr__(field_name, cut_time(value))
        obj.save()

    def to_dobule(str):
        t = json.loads(str.replace("'",'"')) if str else ''

        return t

    def decode_str(obj):
        tmp = []
        for i in obj:
            c = {
            'work':to_dobule(i.work),
            'relax':to_dobule(i.relax),
            'free':to_dobule(i.free),
            'free_tu':to_dobule(i.free_tu),
            'free_we':to_dobule(i.free_we),
            'free_th':to_dobule(i.free_th),
            'free_fr':to_dobule(i.free_fr),
            'free_sa':to_dobule(i.free_sa),
            'free_su':to_dobule(i.free_su),
            'id':i.id,
            'diff_type':i.diff_type,
            'name':i.name
            }
            tmp.append(c)
        return tmp



    ctx = {}
    cardtype = CardType.objects.filter(status=0).all()
    t=2
    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = CardType()
            _save_attr_(r,request)
            save_time(r,request)
            t = int(request.POST.get('diff_type'))

        elif action == 'update':
            id = request.POST.get('id','')
            r = CardType.objects.filter(id=id).first()
            _save_attr_(r,request)
            save_time(r,request)
            t = int(request.POST.get('diff'))

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            t = request.POST.get('type')
            u = CardType.objects.filter(id__in=ids).all()

            for item in u:
                item.status = -1
                item.save()
        elif action == 'select':
            t = request.POST.get('type')

        elif action == 'export':
            w,e = export_excel(cardtype[0],u'卡片类型管理')
            row = 1
            s= ''
            for i  in cardtype:
                w.write(row, 0, i.name)
                w.write(row, 1, i.work)
                w.write(row, 2, i.relax)
                w.write(row, 3, i.get_diff_type_display())
                w.write(row, 4, i.free)
                w.write(row, 5, i.free_tu)
                w.write(row, 6, i.free_we)
                w.write(row, 7, i.free_th)
                w.write(row, 8, i.free_fr)
                w.write(row, 9, i.free_sa)
                w.write(row, 10, i.free_su)
                row +=1
            output = io.BytesIO()
            e.save(output)
            # 重新定位到开始
            output.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=cardtype.xls'
            response.write(output.getvalue())
            return response
              
    if t != 2:
        cardtype = cardtype.filter(diff_type=int(t))
        ctx['type'] = int(t)

    ctx['num'],ctx['num1'] = tim()
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    ctx['cardtype'] = ctx['objects'] = decode_str(cardtype)
    return (ctx,'card_type.html')


@csrf_exempt
@page
def coupon_type(request):
    ''' 优惠券类型设置 ''' 
    
    ctx = {}

    objects = Coupons.objects.all().filter(is_delete=0)

    if request.method == 'POST':
        action = request.POST.get('action', '')
         
        if action == 'add':
             
            r = Coupons()
            _save_attr_(r, request)
 
        elif action == 'update':
            id = request.POST.get('id', '')
            if id:
                r = Coupons.objects.filter(id=int(id)).first()
                _save_attr_(r, request)
             
        elif action == 'search':
            ctx['name'] = name = request.POST.get('name', '')
            ctx['type'] = type = request.POST.get('type', '')
            
            if type:
                objects = objects.filter(type=int(type))
            if name:
                objects = objects.filter(name__contains=name)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Coupons.objects.filter(id__in=ids).update(is_delete=1)
 
    ctx['objects'] = objects.order_by('-update_time')
   
    return (ctx, 'coupon_type.html')


@csrf_exempt
@page
def coupon(request):
    '''优惠券管理'''

    def code(id):
        from meta.qrcode import make_qrcode
        import datetime
        
        url = str(id)
        now = datetime.datetime.now()
        name = str(now.year)+''+str(now.month)+''+str('now.day')+''+str(now.hour)+''+str(now.minute)+''+str(now.second)
        return make_qrcode(url,name+'.png')


    ctx = {}
    objects = TicketRecord.objects.select_related('parkinglot', 'company', 'coupons').all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            id = request.POST.get('id','')
            if id:
                r = TicketRecord.objects.filter(id=id).first()
            else:
                r = TicketRecord()  

            _save_attr_(r, request)

            company_id = request.POST.get('company_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                r.parkinglot_id = int(parkinglot_id)
            if company_id:
                r.company_id = int(company_id)

            ticket_type = request.POST.get('ticket_type', '')
            ticket_id = request.POST.get('ticket_id', '')
            if ticket_type and ticket_id:
                r.coupons_id = int(ticket_id)
            r.coucode = code(r.id)
            r.qrrandom = ran()
            r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Camera.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()
            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()
        elif action == 'search':
            ticket_type = request.POST.get('ticket_type', '')
            ticket_id = request.POST.get('ticket_id', '')

            company_id = request.POST.get('company_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                objects = objects.filter(parkinglot_id=int(parkinglot_id))
                # ctx['gates'] = objects.filter(parkinglot_id=int(parkinglot_id))
            if company_id:
                ctx['company_id'] = int(company_id)
                objects = objects.filter(company_id=int(company_id))
            if ticket_type:
                ctx['ticket_type'] = int(ticket_type)
                objects = objects.filter(ticket_type=int(ticket_type))
                
                ctx['tickets'] = Coupons.objects.filter(is_delete=0, type=int(ticket_type))
             
            if ticket_id:
                ctx['ticket_id'] = int(ticket_id)
                objects = objects.filter(coupons_id=int(ticket_id))

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            TicketRecord.objects.filter(id__in=ids).delete()#update(is_delete=1)

    ctx['objects'] = objects.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    c = Company.objects.select_related('parkinglot').filter(status=1)
    companies = {}

    for i in c:
        if i.parkinglot.id in companies:
            companies[i.parkinglot.id].append({'id': i.id, 'name': i.name})
        else:
            companies[i.parkinglot.id] = [{'id': i.id, 'name': i.name}]
    print(c)
    ctx['all_companies'] = companies

    all_tickets = {}
    all_tickets['0'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=0).order_by('-update_time')]
    all_tickets['1'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=1).order_by('-update_time')]
    all_tickets['2'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=2).order_by('-update_time')]
    all_tickets['3'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=3).order_by('-update_time')]

    ctx['all_tickets'] = all_tickets

    return (ctx, 'coupon.html')


@page
def card(request):
    '''卡片管理'''

    ctx ={}
    cards = Card.objects.filter(status=0).all()
    def correct_obj(request,r):
        # owner_id = request.POST.get('owner', '')
        card_id = request.POST.get('my_card', '')
        suit = request.POST.getlist('suit',[])
        # if owner_id:
        #     p = AdminUser.objects.filter(id=owner_id).first()
        #     if p: 
        #         r.owner = p

        if card_id:
            p = CardType.objects.filter(id=card_id).first()
            if p: 
                r.my_card = p
        r.save()
        if suit:
            for i in suit:
                if i not in r.suit.all():
                    r.suit.add(ParkingLot.objects.filter(id=int(i)).first())
            r.save()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = Card()
            correct_obj(request,r)
            _save_attr_(r, request)
            


        elif action == 'update':
            id = request.POST.get('id','')
            r = Card.objects.filter(id=id).first()
            correct_obj(request,r)
            _save_attr_(r, request)
           

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = Card.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()

        elif action == 'validate':
            owner = request.POST.get('owner', '')
            id = request.POST.get('id','')
            if id:
                r = Card.objects.filter(owner=owner.strip()).exclude(id=int(id),status=0)
            else:   
                r = Card.objects.filter(owner=owner.strip(),status=0)

            if r.exists():
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action == 'export':
            w,e = export_excel(cards[0],u'开卡管理')
            row = 1
            s= ''
            for i  in cards:
                w.write(row, 0, i.owner)
                w.write(row, 1, i.my_card.name)
                w.write(row, 2, i.valid_start)
                w.write(row, 3, i.valid_end)
                for j in i.suit.all():
                    s += j.name+'  '
                w.write(row, 4, s)
                row +=1
            output = io.BytesIO()
            e.save(output)
            # 重新定位到开始
            output.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=card.xls'
            response.write(output.getvalue())
            return response


    ctx['users'] = AdminUser.objects.all()
    ctx['cardtypes'] = CardType.objects.filter(status=0).all()
    ctx['cards'] = ctx['objects'] = cards
    ctx['parkinglot'] = ParkingLot.objects.all()
    return (ctx, 'card.html')


def chargedemo(request):

    ctx = {}
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'charge':
            from .charge import compute, compute_demurrage

            ctx['coupons'] = coupons = request.POST.getlist('coupons', '')
            ctx['in_time'] = in_time = request.POST.get('in_time', '')
            ctx['out_time'] = out_time = request.POST.get('out_time', '')
            ctx['final_out_time'] = final_out_time = request.POST.get('final_out_time', '')
            ctx['car_number'] = car_number = request.POST.get('car_number', '')
            ctx['parkinglot_id'] = parkinglot_id = int(request.POST.get('parkinglot_id', ''))

            ctx['parkinglot'] = parkinglot = ParkingLot.objects.get(id=parkinglot_id)
            ctx['baserule'] = baserule = BaseRule.objects.filter(parkinglot=parkinglot).first()
            ctx['coupons'] = coupons = Coupons.objects.filter(id__in=coupons)
            ctx['card'] = card = parkinglot.parkinglot_card.filter(car_number=car_number).first()

            in_time = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M:%S')
            out_time = datetime.datetime.strptime(out_time, '%Y-%m-%d %H:%M:%S')
            final_out_time = datetime.datetime.strptime(final_out_time, '%Y-%m-%d %H:%M:%S')
            payable, payment, latest_leave_time = compute(parkinglot, in_time, out_time, coupons, card)
            ctx['payment'] = (payable, payment, latest_leave_time)
            ctx['payment_bill2'] = compute_demurrage(parkinglot, out_time, latest_leave_time, card, final_out_time)
            
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    
    all_tickets = {}
    all_tickets['0'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=0).order_by('-update_time')]
    all_tickets['1'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=1).order_by('-update_time')]
    all_tickets['2'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=2).order_by('-update_time')]
    all_tickets['3'] = [{'id': _.id, 'name': _.name} for _ in Coupons.objects.filter(is_delete=0, type=3).order_by('-update_time')]

    ctx['all_tickets'] = all_tickets

    return render(request, 'charge_demo.html', ctx)


@page
@csrf_exempt
def check_coupon(request):
    ctx ={}
    records = TicketRecord.objects.all()

    def t(m):
        return int(m) if m else''

    def c_s(n,s):
        for i in s:
            if i.status == 0:
                    i.status = n
                    i.save()

    if request.method == 'POST':
        action = request.POST.get('action','')
        
        ids = request.POST.getlist('ids','')
        if ids:
            r = TicketRecord.objects.filter(id__in=ids).all()
        if action == 'pass':
            c_s(1,r)

        elif action == 'refuse':
            c_s(2,r)
    
        elif action == 'search':
            p_id = request.POST.get('parkinglot_id','')
            c_id = request.POST.get('company_id','')
            status = request.POST.get('status','')
            records = TicketRecord.objects.all()

            if p_id != '':
                records = records.filter(parkinglot__id=t(p_id))
            if c_id != '':
                records = records.filter(company__id=t(c_id))
            if status != '':
                records = records.filter(status=t(status))
            ctx['p'] = t(p_id)
            ctx['c'] = t(c_id)
            ctx['s'] = t(status)

    ctx['parkinglots'] = ParkingLot.objects.all()
    ctx['companies'] = Company.objects.filter(status=1).all()
    ctx['objects'] = records
    return (ctx,'check_coupon.html')




