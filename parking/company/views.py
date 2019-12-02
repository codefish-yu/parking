from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from administrator.decorators import page, _save_attr_
# Create your views here.


'''合作商户模块'''

@page
def company(request):
	ctx = {}

	def operate_in_batch(status,request):
		ids = request.POST.getlist('ids', '')
		u = Company.objects.filter(id__in=ids).all()
		for item in u:
			item.status = status
			item.save()


	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':
			r = Company()
			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Company.objects.filter(id=id)
			_save_attr_(r.first(), request)
		elif action == 'delete':
			operate_in_batch(-1,request)
			
		elif action == 'inact':
			operate_in_batch(0,request)

		elif action == 'act':
			operate_in_batch(1,request)

		elif action == 'refund':
			r = Refund()
			_save_attr_(r, request)

		elif action == 'validate':
			account = request.POST.get('account','')
			r = Company.objects.filter(account=account.strip())
			if r.exists():
				return JsonResponse({'valid': False})

			return JsonResponse({'valid': True})


	ctx['objects'] = ctx['company'] = Company.objects.exclude(status=-1).all()

	return (ctx,'company.html')