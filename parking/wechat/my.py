from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from realtime.models import InAndOut
from .decorators import user_required, get_park_time



'''用户端 - 我的'''


@user_required
def personal(request, user):
	ctx = { 'menu': 'personal'}
	print(user.wechat_user().head_img)
	ctx['user'] = user

	return render(request, 'public_count/personal/my.html', ctx)


@user_required
def mybill(request, user, id=None):
	ctx = {}
	 
	if id:
		ctx['r'] = r = InAndOut.objects.filter(id=id).first()
		if r:
			ctx['hours1'] = get_park_time(r.in_time, r.out_time)
			ctx['hours2'] = get_park_time(r.out_time, r.final_out_time)
		
		return render(request, 'public_count/personal/bill-detail.html', ctx)

	return render(request, 'public_count/personal/mybill.html', ctx)


@user_required
def mycard(request, user):
	ctx = {}

	from chargerule.models import Card

	plates = MyPlate.objects.filter(user=user)
	plates = [i.plate for i in plates]
	if plates:
		ctx['cards'] = Card.objects.filter(car_number__in=plates)

	return render(request, 'public_count/personal/mycard.html', ctx)


@user_required
def mycoupon(request, user):
	ctx = {}

	 
	return render(request, 'public_count/personal/mycoupon.html', ctx)


@user_required
def myplate(request, user):
	ctx = {}

	plates = MyPlate.objects.filter(user=user)

	if request.method == 'POST':
		action = request.POST.get('action')
		if action == 'bound':
			plate = request.POST.get('plate', '')
			MyPlate.objects.get_or_create(user=user, plate=plate)
		elif action == 'unbound':
			id = request.POST.get('id', '')
			MyPlate.objects.filter(id=id).delete()
		
		return redirect('/wechat/personal/myplate/')
	
	ctx['plates'] = plates
	return render(request, 'public_count/personal/myplate.html', ctx)


@user_required
def bound(request, user):
	return render(request, 'public_count/personal/bound.html')


@user_required
def problem(request, user):
	if request.method == 'POST':
		car_number = request.POST.get('car_number', '')
		gate_id = request.POST.get('gate', '')
		parkinglot_id = request.POST.get('parkinglot', '')

		p = Problem(user=user, plate=car_number, parkinglot_id=parkinglot_id)
		if gate_id:
			p.gate_id = gate_id
		p.save()

		return render(request, 'public_count/problem.html')


@user_required
def scan_coupon(request, user, id, code):

	pass
	
	return render(request, 'public_count/personal/mycoupon.html', ctx)
