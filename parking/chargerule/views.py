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


def coupon_type(request):
    '''优惠券类型设置'''
    pass

    return render(request, 'coupon_type.html')


def card(request):
    '''卡片管理'''
    pass

    return render(request, 'card.html')


def coupon(request):
    '''优惠券管理'''
    pass

    return render(request, 'coupon.html')

