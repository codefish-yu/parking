from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from administrator.decorators import page, _save_attr_
from .models import *
from parkinglot.models import ParkingLot
from administrator.models import AdminUser 


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

    cameras = TicketRecord.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Camera()            
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
            ctx['brand'] = brand = request.POST.get('brand', '')
            ctx['manufacturer'] = manufacturer = request.POST.get('manufacturer', '')
           
            gate_id = request.POST.get('gate_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                cameras = cameras.filter(parkinglot_id=int(parkinglot_id))
                ctx['gates'] = Gate.objects.filter(parkinglot_id=int(parkinglot_id))
            if gate_id:
                ctx['gate_id'] = int(gate_id)
                cameras = cameras.filter(gate_id=int(gate_id))
            if brand:
                cameras = cameras.filter(brand=brand)
            if manufacturer:
                cameras = cameras.filter(manufacturer=manufacturer)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Camera.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Camera.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action == 'get_gate':
            id = request.POST.get('id', '')
            gates = Gate.objects.filter(parkinglot_id=id)
            gates = [{'name': _.name, 'id':_.id} for _ in gates]
            return JsonResponse({'success':True, 'result': gates})

    ctx['objects'] = cameras.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
        
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



