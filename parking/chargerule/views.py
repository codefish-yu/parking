from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


from .models import *
from company.models import Company
from parkinglot.models import ParkingLot
from administrator.models import AdminUser 
from administrator.decorators import page, _save_attr_


'''计费规则管理'''


def base_rule(request):
    '''基本计费规则配置'''
    pass

    return render(request, 'base_rule.html')
@page
def card_type(request):
    '''卡片类型设置'''

    ctx = {}


    def correct_card_type(request,obj):
        name = request.POST.get('name')
        rule = request.POST.get('rule')
        suit = request.POST.getlist('suit',[])

        obj.name = name if name else ''
        obj.rule = rule if rule else ''
        obj.save()
        obj.suit.clear()

        for i in suit:
            obj.suit.add(ParkingLot.objects.filter(id=int(i)).first())

        obj.save()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = CardType()
            correct_card_type(request,r)

        if action == 'update':
            id = request.POST.get('id','')
            r = CardType.objects.filter(id=id).first()
            correct_card_type(request,r)

        if action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = CardType.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()

    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    ctx['cardtype'] = ctx['objects'] = CardType.objects.filter(status=0).all()
    return (ctx,'card_type.html')


@csrf_exempt
@page
def coupon_type(request):
    ''' 优惠券类型设置 ''' 
    
    ctx = {}

    objects = []

    if request.method == 'POST':
        action = request.POST.get('action', '')
        ctx['type'] = type = request.POST.get('type', '')
        type = int(type)
        print(type)
        if type == 0:
            R = Discount
        elif type == 1:
            R = Voucher
        elif type == 2:
            R = Coupon
        else:
            R = HourTicket
        objects = R.objects.all().filter(is_delete=0)

        if action == 'add':
             
            r = R()
            _save_attr_(r, request)
 
        elif action == 'update':
            id = request.POST.get('id', '')

            r = R.objects.filter(id=id).first()
            _save_attr_(r, request)
             
        elif action == 'search':
            ctx['name'] = name = request.POST.get('name', '')
            forbidden = request.POST.get('forbidden', '')
            parkinglot = request.POST.get('parkinglot', '')

            if forbidden:
                ctx['forbidden'] = int(forbidden)
                workers = objects.filter(forbidden=int(forbidden))
            if parkinglot:
                ctx['parkinglot'] = int(parkinglot)
                workers = objects.filter(parkinglot_id=int(parkinglot))
            if name:
                objects = objects.filter(name__contains=name)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            R.objects.filter(id__in=ids).update(is_delete=1)

        # elif action == 'forbidden':
        #     id = request.POST.get('id', '')
        #     Worker.objects.filter(id=id).update(forbidden=1)
        #     return JsonResponse({'success': True})

        # elif action == 'awaken':
        #     id = request.POST.get('id', '')
        #     Worker.objects.filter(id=id).update(forbidden=0)
        #     return JsonResponse({'success': True})

        # elif action == 'validate':
        #     number = request.POST.get('number', '')
        #     id = request.POST.get('id', '')

        #     r = Worker.objects.filter(number=number.strip())
        #     if r.exists():
        #         if id:
        #             if r.first().id != int(id):
        #                 return JsonResponse({'valid': False})
        #         else:
        #             return JsonResponse({'valid': False})

        #     return JsonResponse({'valid': True})

    ctx['objects'] = objects
   
    return (ctx, 'coupon_type.html')


@csrf_exempt
@page
def coupon(request):
    '''优惠券管理'''

    ctx = {}

    objects = TicketRecord.objects.select_related('parkinglot', 'company', 'discount', 'voucher', 'coupon', 'hourticket').all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
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
                r.type = int(ticket_type)
                if ticket_type == '0':
                    r.discount_id = int(ticket_id)
                elif ticket_type == '1':
                    r.voucher_id = int(ticket_id)
                elif ticket_type == '2':
                    r.coupon_id = int(ticket_id)
                elif ticket_type == '3':
                    r.hourticket = int(ticket_id)
            
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
                if ticket_type == '0':
                    ctx['tickets'] = Discount.objects.filter(is_delete=0)
                elif ticket_type == '1':
                    ctx['tickets'] = Voucher.objects.filter(is_delete=0)
                elif ticket_type == '2':
                    ctx['tickets'] = Coupon.objects.filter(is_delete=0)
                elif ticket_type == '3':
                    ctx['tickets'] = HourTicket.objects.filter(is_delete=0)
            if ticket_id:
                ctx['ticket_id'] = int(ticket_id)
                objects = objects.filter(Q(discount_id=int(ticket_id)) | Q(voucher_id=int(ticket_id)) | Q(coupon_id=int(ticket_id)) | Q(hourticket_id=int(ticket_id)))

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            TicketRecord.objects.filter(id__in=ids).delete()#update(is_delete=1)

        # elif action == 'validate':
        #     number = request.POST.get('number', '')
        #     id = request.POST.get('id', '')

        #     r = Camera.objects.filter(number=number.strip())
        #     if r.exists():
        #         if id:
        #             if r.first().id != int(id):
        #                 return JsonResponse({'valid': False})
        #         else:
        #             return JsonResponse({'valid': False})

        #     return JsonResponse({'valid': True})


    ctx['objects'] = objects.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    ctx['companies'] = Company.objects.filter(status=0)

    all_tickets = {}
    all_tickets['0'] = [{'id': _.id, 'name': _.name} for _ in Discount.objects.filter(is_delete=0).order_by('-update_time')]
    all_tickets['1'] = [{'id': _.id, 'name': _.name} for _ in Voucher.objects.filter(is_delete=0).order_by('-update_time')]
    all_tickets['2'] = [{'id': _.id, 'name': _.name} for _ in Coupon.objects.filter(is_delete=0).order_by('-update_time')]
    all_tickets['3'] = [{'id': _.id, 'name': _.name} for _ in HourTicket.objects.filter(is_delete=0).order_by('-update_time')]

    ctx['all_tickets'] = all_tickets

    return (ctx, 'coupon.html')


@page
def card(request):
    '''卡片管理'''

    ctx ={}
    def correct_obj(request,r):
        owner_id = request.POST.get('owner', '')
        card_id = request.POST.get('my_card', '')
        if owner_id:
            p = AdminUser.objects.filter(id=owner_id).first()
            if p: 
                r.owner = p

        if my_card:
            p = CardType.objects.filter(id=card_id).first()
            if p: 
                r.owner = p
        r.save()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = CardType()
            correct_obj(request,r)
            _save_attr_(r, request)


        if action == 'update':
            id = request.POST.get('id','')
            r = Card.objects.filter(id=id).first()
            correct_obj(request,r)
            _save_attr_(r, request)

        if action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = Card.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()


    ctx['users'] = AdminUser.objects.all()
    ctx['cardtypes'] = CardType.objects.filter(status=0).all()
    ctx['cards'] = ctx['objects'] = Card.objects.filter(status=0).all()
    return (ctx, 'card.html')



