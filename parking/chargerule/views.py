from django.shortcuts import render

# Create your views here.

from .models import *


'''计费规则管理'''


def base_rule(request):
    '''基本计费规则配置'''
    pass

    return render(request, 'base_rule.html')

def card_type(request):
    '''卡片类型设置'''
    pass
    
    return render(request, 'card_type.html')


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

