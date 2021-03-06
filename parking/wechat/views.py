from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .my import *
from meta import api
from device.models import Camera
from .decorators import *
from parkinglot.models import ParkingLot
from meta.models import Product, Order, User
from chargerule.charge import charge, demurrage
from realtime.models import InAndOut, Bill, OpeningOrder


import math
import datetime


'''手机客户端 ''' 


# 创建开闸指令
def createOpenOrder(parkinglot_id, gate_id, in_and_out):
    if OpeningOrder.objects.filter(gate_id=gate_id).exists():
        order = OpeningOrder.objects.filter(gate_id=gate_id).first()
        order.status = 2
        order.in_and_out = in_and_out
        order.save()
    else:
        OpeningOrder.objects.create(parkinglot_id=parkinglot_id, gate_id=gate_id, status=2, in_and_out=in_and_out)


# 计费
def createBill(in_and_out, coupons=None):

    #  根据出入场的时间in_time, out_time , number, 计算收费
    payable, payment, latest_leave_time = charge(in_and_out, coupons)

    if not in_and_out.bill:
        bill = Bill(payable=payable, payment=0.01, status=1 if payment == 0 else 0, pay_time=now())
        product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='parking')
    
        bill.product = product
        bill.save()
    else:
        bill = in_and_out.bill
        bill.payable = payable
        bill.payment=payment
        bill.status=1 if payment == 0 else 0
        bill.pay_time=now()
        bill.save()
        product = bill.product
        product.price = payment
    in_and_out.latest_leave_time = latest_leave_time
    in_and_out.bill = bill
    in_and_out.save()

    return bill


# 计算滞留费
def createBill2(in_and_out):
    payment = demurrage(in_and_out)
    if not in_and_out.bill2:
        bill = Bill(payable=payment, payment=0.01, status=0)
        product = Product.objects.create(price=payment, name='parking fee', company='jieting', category='parking')
        bill.product = product
        bill.save()
    else:
        bill = in_and_out.bill
        bill.payable = payment
        bill.payment = payment
        bill.save()
        product = bill.product
        product.price = payment
        product.save()
    in_and_out.bill2 = bill
    in_and_out.save()

    return bill


def cost_coupons(coupons, bill):
    if coupons:
        from chargerule.models import UserCoupon
        usercoupons = UserCoupon.objects.filter(id__in=coupons)
        usercoupons.update(status=1)
        bill.user_coupon = usercoupons
    return


@user_required
def parkin(request, user, parkinglot_id, gate_id):
    '''卡口扫码入场'''
 
    camera = Camera.objects.filter(gate_id=gate_id).first()

    r = InAndOut.objects.filter(parkinglot_id=parkinglot_id, camera_in=camera, user=user, status__lte=0).first()
    if not r:
        r = InAndOut.objects.create(
            status=-1, # -1  等待开闸入场
            user=user, 
            enter_type=1, 
            camera_in=camera,
            parkinglot_id=parkinglot_id, 
            in_time=now()
        )

    createOpenOrder(parkinglot_id, gate_id, r)

    ctx = {'r': r, 'menu': 'park', 'hours': get_park_time(r.in_time) }

    return render(request, 'public_count/in.html', ctx)


@user_required
def parkout(request, user, parkinglot_id, gate_id=None):
    '''场内扫码支付 或 卡口扫码支付出场'''

    ctx = {'parkinglot_id': parkinglot_id, 'menu': 'park'}

    ctx['parkinglot'] = ParkingLot.objects.filter(id=parkinglot_id).first()
    if gate_id:
        ctx['gate_id'] = gate_id

    r = InAndOut.objects.filter(parkinglot_id=parkinglot_id, user=user, status=0).order_by('-in_time').first()#status=0

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'payconfirm':  # 支付成功后确认账单状态
            product_id = request.POST.get('product_id', '')
            if product_id:
                order = Order.objects.filter(product_id=product_id).order_by('-create_time').first()
                if order:
                    from meta.models import Payment
                    if Payment.objects.filter(order=order).exists():
                        

                        bill = Bill.objects.filter(product_id=int(product_id))
                        bill.update(status=1, pay_type=1, pay_time=now())
                        
                        bill = bill.first()
                        coupons = request.POST.get('coupons', [])
                        cost_coupons(coupons, bill)

                        if gate_id:  # 如果此时在出口扫描支付, 则要立即创建开闸指令
                            r = bill.InAndOut
                            createOpenOrder(parkinglot_id, gate_id, r)

                        return JsonResponse({'success': True})
            return JsonResponse({'success': False})

        if action == 'record':
            # 输入车牌查询入场记录
            ctx['car_number'] = car_number = request.POST.get('car_number', '')
             
            r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), number=car_number, status=0).order_by('-in_time')
            if r.exists():
                r = r.first()
                
                MyPlate.objects.get_or_create(user=user, plate=r.number)
                r.user = user
                r.save()
                ctx['r'] = r
                ctx['hours'] = get_park_time(r.in_time)

                return render(request, 'public_count/2_parking_hours.html', ctx)
            else:
                ctx['error'] = '未匹配到入场车牌！请核对车牌。'
                return render(request, 'public_count/1_plate_number.html', ctx)

        if action == 'leave':
            # 点击结算出场, 计算
            id = request.POST.get('id', '')

            r = InAndOut.objects.filter(id=int(id)).first()
 
            if gate_id:
                camera = Camera.objects.filter(gate_id=gate_id).first()
                r.camera_out = camera
            r.out_time = now()
            r.leave_type = 1
           
            r.save()

            bill = createBill(r)
            ctx['payment'] = (bill.payment, bill.payable)

            ctx['r'] = r
            ctx['hours'] = get_park_time(r.in_time,r.out_time)
            ctx['product'] = bill.product
            
            return render(request, 'public_count/3_pay_bill1.html', ctx)

        if action == 'coupons_charge':
            # 用券。 用户在结算支付页面, 选择优惠券进行重新计算费用
            coupons = request.POST.getlist('coupons', '')
            id = request.POST.get('id', '')
            r = InAndOut.objects.filter(id=int(id)).first()

            coupons = [Coupons.objects.get(id=_) for _ in coupons]
            bill = createBill(r, coupons)
            
            ctx['payment'] = bill.payment
            ctx['payable'] = bill.payable

            return JsonResponse(ctx)

    ''' 扫码执行入口'''
    if not r:     # 如果根据用户查不到记录就让其输入车牌号
        ctx['plates'] = MyPlate.objects.filter(user=user)
        return render(request, 'public_count/1_plate_number.html', ctx)
    else:         # 如果有停车记录跳至记录页面, 可以点击离场
        
        if not r.bill:
            print('xx')
            if gate_id:
                if not r.out_time:
                    r.out_time = now()
                    r.save()
                payment = charge(r)[1]
                if payment == 0:      # 1.没产生费用, 开闸
                    createOpenOrder(parkinglot_id, gate_id, r)
                    r.final_out_time = now()
                    r.save()
                    return render(request, 'public_count/no_fee.html', ctx)

        else:
            print(r.bill.status, 'xxxxx')
            if r.bill.status == 1:
                if gate_id:
                    print('xxx') 
                    if not r.bill2:
                        print('sss') 
                        payment = demurrage(r) # 2.滞留费为0, 开闸
                        if payment == 0:
                            print('qqq') 

                            createOpenOrder(parkinglot_id, gate_id, r)
                            r.final_out_time = now()
                            r.save()
                        else:
                            bill = createBill2(r)  # 有滞留费
                            print('bill')
                            print(bill.payment)
                            ctx['hours'] = get_park_time(r.out_time, now())
                            ctx['payment'] = bill.payment
                            ctx['payable'] = bill.payable
                            ctx['r'] = r
                            ctx['product'] = bill.product

                            return render(request, 'public_count/5_pay_bill2.html', ctx) 
                    else:
                        print(r.bill2.status)
                        print(r.bill2.id)
                        print('r.bill2.status')
                        if r.bill2.status == 1: # 3. 已支付滞留费, 开闸
                            createOpenOrder(parkinglot_id, gate_id, r)
                        else:
                            bill = createBill2(r)
                            ctx['hours'] = get_park_time(r.out_time, now())
                            ctx['payment'] = bill.payment
                            ctx['payable'] = bill.payable
                            ctx['r'] = r
                            ctx['product'] = bill.product
                            
                            return render(request, 'public_count/5_pay_bill2.html', ctx)

                # 场内支付成功提示
                return render(request, 'public_count/4_pay_success.html', ctx)
        print('hours')
        ctx['r'] = r
        ctx['hours'] = get_park_time(r.in_time)

        return render(request, 'public_count/2_parking_hours.html', ctx)


