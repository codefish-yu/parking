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
        if type == 0:
            objects = Discount.objects.all().filter(is_delete=0)
        elif type == 1:
            objects = Voucher.objects.all().filter(is_delete=0)
        elif type == 2:
            objects = Coupon.objects.all().filter(is_delete=0)
        else:
            objects = HourTicket.objects.all().filter(is_delete=0)

        if action == 'add':
            if type == 0:
                r = Discount()
            elif type == 1:
                r = Voucher()
            elif type == 2:
                r = Coupon()
            else:
                r = HourTicket()

            _save_attr_(r, request)
 
        elif action == 'update':
            id = request.POST.get('id', '')

            r = Worker.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

        elif action == 'search':
            ctx['name'] = name = request.POST.get('name', '')
            ctx['number'] = number = request.POST.get('number', '')
            forbidden = request.POST.get('forbidden', '')
            parkinglot = request.POST.get('parkinglot', '')

            if forbidden:
                ctx['forbidden'] = int(forbidden)
                workers = workers.filter(forbidden=int(forbidden))
            if parkinglot:
                ctx['parkinglot'] = int(parkinglot)
                workers = workers.filter(parkinglot_id=int(parkinglot))
            if number:
                workers = workers.filter(number__contains=number)
            if name:
                workers = workers.filter(name__contains=name)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            if type == 0:
                Discount.objects.filter(id__in=ids).update(is_delete=1)
            elif type == 1:
                Voucher.objects.filter(id__in=ids).update(is_delete=1)
            elif type == 2:
                Coupon.objects.filter(id__in=ids).update(is_delete=1)
            else:
                HourTicket.objects.filter(id__in=ids).update(is_delete=1)

        elif action == 'forbidden':
            id = request.POST.get('id', '')
            Worker.objects.filter(id=id).update(forbidden=1)
            return JsonResponse({'success': True})

        elif action == 'awaken':
            id = request.POST.get('id', '')
            Worker.objects.filter(id=id).update(forbidden=0)
            return JsonResponse({'success': True})

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Worker.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

    ctx['objects'] = objects
   
    return (ctx, 'coupon_type.html')

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

        if card_id:
            p = CardType.objects.filter(id=card_id).first()
            if p: 
                r.my_card = p
        r.save()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = Card()
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


def coupon(request):
    '''优惠券管理'''
    pass

    return render(request, 'coupon.html')

