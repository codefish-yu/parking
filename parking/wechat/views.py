from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from meta import api
from meta.models import Product, Order
#from meta.decorators import user_required
from realtime.models import InAndOut, Bill, OpeningOrder


import datetime
import functools


'''手机客户端 ''' 
def user_required(func):

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        from meta import api
        
        wrapper.__name__ = func.__name__

        token = request.session['token'] if 'token' in request.session else ''
        
        if not token:
            token = request.GET.get('token', '')
            if token:
                request.session['token'] = token

        next_url = request.get_full_path()

        if not token:
            return redirect('/login/public/account/?next=' + next_url)

        try:
            user = api.check_token(token)
        except APIError:
            return redirect('/login/public/account/?next=' + next_url)

        request.user = user
        result = func(request, user=user, *args, **kwargs)
        return result

    return wrapper

# 创建开闸指令
def createOpenOrder(parkinglot_id, gate_id, in_and_out):
    in_and_out.final_out_time = datetime.datetime.now()
    in_and_out.save()

    if OpeningOrder.objects.filter(gate_id=gate_id).exists():
        order = OpeningOrder.objects.filter(gate_id=gate_id).first()
        order.status = 2
        order.in_and_out = in_and_out
        order.save()
    else:
        OpeningOrder.objects.create(parkinglot_id=parkinglot_id, gate_id=gate_id, status=2, in_and_out=in_and_out)



def createBill(in_and_out):
    pass
    #  根据出入场的时间in_time, out_time , number, 计算收费

    bill = Bill(payable=0.01, payment=0.01, status=0, pay_time=datetime.datetime.now())
    bill.save()
    in_and_out.bill = bill
    in_and_out.save()

    product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='park')
    
    bill.product = product
    bill.save()

    return bill


@user_required
def parkin(request, user, parkinglot_id, gate_id):
    '''卡口扫码入场'''

    r = InAndOut.objects.filter(parkinglot_id=parkinglot_id, gate_in_id=gate_id, user=user, status__lte=0).first()
    if not r:
        r = InAndOut.objects.create(
            status=-1, # -1  等待开闸入场
            user=user, 
            enter_type=1, 
            gate_in_id=gate_id,
            parkinglot_id=parkinglot_id, 
            in_time=datetime.datetime.now(),
        )
    createOpenOrder(parkinglot_id, gate_id, r)

    ctx = {'r': r}
    return render(request, 'public_count/in.html', ctx)


@user_required
def parkout(request, user, parkinglot_id, gate_id=None):
    '''卡口扫码出场'''
    ctx = {'parkinglot_id': parkinglot_id}
    if gate_id:
        ctx['gate_id'] = gate_id

    r = InAndOut.objects.filter(parkinglot_id=parkinglot_id, user=user, status=0).order_by('-in_time').first()

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
                        bill.update(status=1, pay_type=1, pay_time=datetime.datetime.now())
                        
                        if gate_id:  # 如果此时在出口扫描支付, 则要立即创建开闸指令
                            r = bill.first().InAndOut
                            createOpenOrder(parkinglot_id, gate_id, r)

                        return JsonResponse({'success': True})
            return JsonResponse({'success': False})

        if action == 'record':
            # 输入车牌查询入场记录
            ctx['car_number'] = car_number = request.POST.get('car_number', '')
             
            r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), number=car_number, status=0).order_by('-in_time')
            if r.exists():
                r = r.first()
                r.user = user
                r.save()
                ctx['record'] = r
                return render(request, 'public_count/number2.html', ctx)
            else:
                ctx['msg'] = '无入场记录'
                return render(request, 'public_count/error.html', ctx)

        if action == 'leave':
            # 点击离场, 计算
            id = request.POST.get('id', '')

            r = InAndOut.objects.filter(id=int(id))
            if r:
                # 计算费用
                r = r.first()

                r.out_time = datetime.datetime.now()
                r.leave_type = 1
               
                r.save()

                bill = createBill(r)
                
                ctx['record'] = r
                ctx['product'] = bill.product

                return render(request, 'public_count/number3.html', ctx)

    if not r:     # 如果查不到记录就让其输入车牌号
        return render(request, 'public_count/number1.html', ctx)
    else:         # 如果有记录跳至记录页面, 可以点击离场

        if r.bill:
            if r.bill.status == 0: # 未支付
                r.out_time = datetime.datetime.now()
                r.leave_type = 1
               
                r.save()
                bill = createBill(r)

                ctx['record'] = r
                ctx['product'] = bill.product

                return render(request, 'public_count/number3.html', ctx)
            else:   # 已支付
                if gate_id: # 抬杆离场
                    createOpenOrder(parkinglot_id, gate_id, r)
                # 场内支付成功提示
                return render(request, 'public_count/number4.html', ctx)

        ctx['record'] = r
        return render(request, 'public_count/number2.html', ctx)



# @user_required
# def leave(request, user, parkinglot_id):
#     ctx = {}

#     token = request.session['token']
    
#     ctx['parkinglot_id'] = parkinglot_id

#     r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), user=user, status=0).order_by('-in_time')
#     if r.exists():
#         r = r.first()
#         if r.bill:
#             if r.bill.status == 0:
#                 ctx['record'] = r
#                 return render(request, 'public_count/number3.html', ctx)
#             else:
#                 return render(request, 'public_count/number4.html', ctx)
#         else:
#             bill = Bill(
#                 payable=0.01, 
#                 payment=0.01, 
#                 pay_time=datetime.datetime.now(),
#                 status=0
#             )
#             bill.save()
#             r.bill = bill
#             r.save()

#             product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='park')
            
#             bill.product = product
#             bill.save()
            
#             ctx['record'] = r
#             ctx['product'] = product

#             return render(request, 'public_count/number3.html', ctx)

#     if request.method == 'POST':
#         action = request.POST.get('action', '')
#         print(action)
#         if action == 'record':
#             ctx['car_number'] = car_number = request.POST.get('car_number', '')
#             print(car_number)
#             r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), number=car_number).order_by('-in_time')
#             print(r)
#             if r: 
#                 r = r.first()

#                 if not r.bill or r.bill.status == 0:
                    
#                     ctx['record'] = r
#                     return render(request, 'public_count/number2.html', ctx)
        
#         elif action == 'leave':
            
#             id = request.POST.get('id', '')

#             r = InAndOut.objects.filter(id=int(id))
#             if r:
#                 # 计算费用
#                 r = r.first()

#                 bill = Bill(
#                     payable=0.01, 
#                     payment=0.01, 
#                     pay_time=datetime.datetime.now(),
#                     status=0
#                 )
#                 bill.save()
#                 r.bill = bill
#                 r.save()

#                 product = Product.objects.create(price=bill.payment, name='parking fee', company='jietingkeji', category='park')
                
#                 bill.product = product
#                 bill.save()
                
#                 ctx['record'] = r
#                 ctx['product'] = product

#                 return render(request, 'public_count/number3.html', ctx)

#         elif action == 'payconfirm':
#             product_id = request.POST.get('product_id', '')
#             if product_id:
#                 order = Order.objects.filter(product_id=product_id).order_by('-create_time').first()
#                 if order:
#                     from meta.models import Payment
#                     if Payment.objects.filter(order=order).exists():
#                         Bill.objects.filter(product_id=int(product_id)).update(status=1, pay_type=1, pay_time=datetime.datetime.now())
#                         return JsonResponse({'success': True})
#             return JsonResponse({'success': False})
#     return render(request, 'public_count/number1.html', ctx)