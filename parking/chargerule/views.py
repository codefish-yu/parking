from django.shortcuts import render

# Create your views here.
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


def coupon_type(request):
    '''优惠券类型设置'''
    pass

    return render(request, 'coupon_type.html')

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


def coupon(request):
    '''优惠券管理'''
    pass

    return render(request, 'coupon.html')

