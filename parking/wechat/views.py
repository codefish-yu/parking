from django.shortcuts import render, redirect


from meta import api
from meta.models import Product, Order
from realtime.models import InAndOut


import functools


'''手机客户端 ''' 

from meta.decorators import user_required
# def user_required(func):

#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
        
#         wrapper.__name__ = func.__name__

#         token = request.session['token'] if 'token' in request.session else ''
        
#         if not token:
#             next_url = request.get_full_path()
#             return redirect('/login/public/account/?next=' + next_url)

#         try:
#             user = api.check_token(token)
#         except APIError:
#             return redirect('/login/public/account/?next=' + next_url)

#         request.user = user
#         result = func(request, user=user, *args, **kwargs)
#         return result

#     return wrapper


def enter(request):
    '''无牌车扫码入场'''
    token = request.session['token']
    user = api.check_token(token)

    parkinglot_id = request.GET.get('parkinglot_id', '')

    if parkinglot_id:
        
        r = InAndOut.objects.filter(parkinglot_id=int(parkinglot_id), user=user)

        if r: 
            r = r.first()
            if r.bill.status == 0:
                pass

    else:
        ctx['error'] = '车场不存在'

    return render(request, 'public_count/index.html', ctx)


@user_required
def leave(request, user, parkinglot_id):
    ctx = {}

    token = request.session['token']
    
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

                product = Product.objects.create(price=bill.payment, name='停车费用', company='杰停科技', category='停车服务')
                order = Order.objects.create(user=user, price=bill.payment, product=product)
                
                bill.product = product
                bill.save()
                
                ctx['record'] = r
                ctx['order'] = order

                return render(request, 'public_count/number3.html', ctx)


    return render(request, 'public_count/number1.html', ctx)


