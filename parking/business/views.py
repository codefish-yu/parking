from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from chargerule.models import TicketRecord
from company.models import Company
from meta.models import Product,Order,Payment
from django.http import JsonResponse
from meta import api

# Create your views here.
def wuser_required(func):

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


def user_required(view_func):

    def wrapper(request, *args, **kwargs):
        if 'company_id' not in request.session:
            return redirect('/business/com_login/')

        company = Company.objects.filter(id=request.session['company_id']).first()
        return view_func(request, company=company, *args, **kwargs)

    return wrapper

# @wuser_required
@csrf_exempt
def com_login(request):

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'login':
			account = request.POST.get('account')
			password = request.POST.get('password')
			company = Company.objects.filter(account=account,password=password,status=1).first()
			if company:
				request.session['company_id'] = company.id
				return redirect('/business/grant/')
			else:
				return redirect('/business/com_login/')

	return render(request,'com_login.html')


@csrf_exempt
def apply(request,tc_id):
	ctx = {}
	tip = -1
	record = TicketRecord.objects.filter(id=int(tc_id)).first()
	
	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'buy':
			amount = request.POST.get('amount')
			cost = float(request.POST.get('cost'))
			print(cost)
			r = ApplyRecord()
			r.coupon = record
			r.number = int(amount)
			b = BusinessBill()
			p = Product()
			b.cost=cost
			p.price=cost
			if cost == 0:
				b.status =1
				record.extra +=int(amount)
				record.save() 
			p.save()
			b.product = p
			b.save()
			r.bill = b
			r.save()
			tip = p.id
			if cost == 0:
				return redirect('/business/grant/')

			

		elif action == 'confirm':
			p_id = request.POST.get('product_id')
			if p_id:
				order = Order.objects.filter(product_id=pid).order_by('-create_time').first()
				if order:
					if Payment.objects.filter(order=order).exists():
						bill = BusinessBill.objects.filter(product_id=int(p_id))
						bill.update(status=1, pay_type=1, pay_time=datetime.datetime.now())
						ar = ApplyRecord.objects.filter(product__id=p_id).first()
						record.extra +=ar.number
						record.save()

						return JsonResponse({'result':'ok'})
			return JsonResponse({'result':'bad'})

	ctx['product_id'] = tip
	ctx['diff'] = record.amount - record.extra
	ctx['record'] = record
	return render(request,'apply.html',ctx)



@csrf_exempt
@user_required
def grant(request,company):
	ctx = {}
	p=0
	records = TicketRecord.objects.filter(company=company).all()


	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'change':
			p = int(request.POST.get('p'))
			if p == 0:
				records = TicketRecord.objects.filter(company=company).all()
			else:
				records = ApplyRecord.objects.filter(coupon__company=company).all()


	ctx['p']=p
	ctx['records'] = records
	return render(request,'grant.html',ctx) 
