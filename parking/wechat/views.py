from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from meta import api
from meta.models import Product, Order
from meta.decorators import user_required
from realtime.models import InAndOut, Bill, OpeningOrder


import datetime
import functools


'''手机客户端 ''' 


@user_required
def parkin(request, user, parkinglot_id, gate_id):
    '''卡口扫码入场'''

    if not InAndOut.objects.filter(parkinglot_id=parkinglot_id, gate_in_id=gate_id, user=user, status=0).exists():
        InAndOut.objects.create(
            user=user, 
            enter_type=1, 
            gate_in_id=gate_id,
            parkinglot_id=parkinglot_id, 
            in_time=datetime.datetime.now(),
        )
    OpeningOrder.objects.create(parkinglot_id=parkinglot_id, gate_id=gate_id, status=2)
    return render(request, 'public_count/in.html')

# def user_required(func):

#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
        
#         wrapper.__name__ = func.__name__

#         token = request.session['token'] if 'token' in request.session else ''
        
#         if not token:
#             next_url = request.get_full_path()
#             print(next_url)
#             return redirect('/login/public/account/?next=' + next_url)
#         try:
#             user = api.check_token(token)
#         except APIError:
#             print('error')
#             return redirect('/login/public/account/?next=' + next_url)
#         request.user = user
#         result = func(request, user=user, *args, **kwargs)
#         return result

#     return wrapper


@user_required
def parkout(request, user, parkinglot_id, gate_id):
    '''卡口扫码出场'''
    ctx = {'parkinglot_id': parkinglot_id, 'gate_id': gate_id}

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'payconfirm':
            product_id = request.POST.get('product_id', '')
            if product_id:
                order = Order.objects.filter(product_id=product_id).order_by('-create_time').first()
                if order:
                    from meta.models import Payment
                    if Payment.objects.filter(order=order).exists():
                        Bill.objects.filter(product_id=int(product_id)).update(status=1, pay_type=1, pay_time=datetime.datetime.now())
                        OpeningOrder.objects.create(parkinglot_id=parkinglot_id, gate_id=gate_id, status=2)
                        
                        return JsonResponse({'success': True})
            return JsonResponse({'success': False})

    r = InAndOut.objects.filter(parkinglot_id=parkinglot_id, user=user, status=0).order_by('-in_time').first()

    if r:
        r.gate_out_id = gate_id
        r.out_time = datetime.datetime.now()
        r.leave_type = 1

        r.save()

        if r.bill: 
            if r.bill.status == 1:  # 已支付
                OpeningOrder.objects.create(parkinglot_id=parkinglot_id, gate_id=gate_id, status=2)
            else: 
               # 未支付
                bill = r.bill
                
                ctx['record'] = r
                ctx['product'] = bill.product

                return render(request, 'public_count/scan_pay.html', ctx)  
        else:
            # 未结算订单
            bill = Bill(
                payable=0.01, 
                payment=0.01, 
                pay_time=datetime.datetime.now(),
                status=0
            )
            bill.save()
            r.bill = bill
            r.save()

            product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='park')
            
            bill.product = product
            bill.save()
            
            ctx['record'] = r
            ctx['product'] = product

            return render(request, 'public_count/scan_pay.html', ctx)

    return render(request, 'public_count/out.html', ctx)


@user_required
def leave(request, user, parkinglot_id):
    ctx = {}

    token = request.session['token']
    
    ctx['parkinglot_id'] = parkinglot_id

    r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), user=user).order_by('in_time')
    if r.exists():
        r = r.first()
        if r.bill and r.bill.status == 0:
            ctx['record'] = r
            return render(request, 'public_count/number3.html', ctx)

    if request.method == 'POST':
        action = request.POST.get('action', '')
        print(action)
        if action == 'record':
            ctx['car_number'] = car_number = request.POST.get('car_number', '')
            print(car_number)
            r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), number=car_number).order_by('-in_time')
            print(r)
            if r: 
                r = r.first()

                if not r.bill or r.bill.status == 0:
                    
                    ctx['record'] = r
                    return render(request, 'public_count/number2.html', ctx)
        
        elif action == 'leave':
            
            id = request.POST.get('id', '')

            r = InAndOut.objects.filter(id=int(id))
            if r:
                # 计算费用
                r = r.first()

                bill = Bill(
                    payable=0.01, 
                    payment=0.01, 
                    pay_time=datetime.datetime.now(),
                    status=0
                )
                bill.save()
                r.bill = bill
                r.save()

                product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='park')
                
                bill.product = product
                bill.save()
                
                ctx['record'] = r
                ctx['product'] = product

                return render(request, 'public_count/number3.html', ctx)

        elif action == 'payconfirm':
            product_id = request.POST.get('product_id', '')
            if product_id:
                order = Order.objects.filter(product_id=product_id).order_by('-create_time').first()
                if order:
                    from meta.models import Payment
                    if Payment.objects.filter(order=order).exists():
                        Bill.objects.filter(product_id=int(product_id)).update(status=1, pay_type=1, pay_time=datetime.datetime.now())
                        return JsonResponse({'success': True})
            return JsonResponse({'success': False})
    return render(request, 'public_count/number1.html', ctx)


