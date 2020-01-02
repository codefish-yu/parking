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

	if request.method == 'POST':
		action = request.POST.get('action')
		pass


	return render(request, 'public_count/personal/mycard.html', ctx)


@user_required
def mycoupon(request, user):
	ctx = {}

	if request.method == 'POST':
		action = request.POST.get('action')
		pass


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


	return render(request, 'public_count/personal/myplate.html', ctx)



