from django.shortcuts import render

# Create your views here.
from administrator.decorators import page, _save_attr_
from .models import *


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
        # suit = request.POST

        obj.name = name if name else null
        obj.rule = rule if rule else null
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


    ctx['cardtype'] = ctx['objects'] = CardType.objects.all()
    return (ctx,'card_type.html')


@csrf_exempt
@page
def coupon_type(request):
    ''' 优惠券类型设置 ''' 
    
    ctx = {}

    objects = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        ctx['type'] = type = request.POST.get('type', '')

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
            Worker.objects.filter(id__in=ids).update(is_delete=1)

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

    ctx['objects'] = workers
   
    return (ctx, 'worker.html')

    return render(request, 'coupon_type.html')


def card(request):
    '''卡片管理'''
    pass

    return render(request, 'card.html')


def coupon(request):
    '''优惠券管理'''
    pass

    return render(request, 'coupon.html')

