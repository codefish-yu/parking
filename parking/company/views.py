from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from administrator.decorators import page, _save_attr_
from parkinglot.models import ParkingLot
# Create your views here.
import io
import xlwt


'''合作商户模块'''

@page
def company(request):
	ctx = {}
	companys = Company.objects.exclude(status=-1).all()

	def operate_in_batch(status,request):
		ids = request.POST.getlist('ids', '')
		u = Company.objects.filter(id__in=ids).all()
		for item in u:
			item.status = status
			item.save()
	def op(r,request):
		parking = request.POST.get('suit')
		if parking:
			r.parkinglot = ParkingLot.objects.filter(id=int(parking)).first()
			r.save()



	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':
			r = Company()
			_save_attr_(r, request)
			op(r,request)

		elif action == 'update':
			id = request.POST.get('id', '')
			r = Company.objects.filter(id=id).first()
			_save_attr_(r,request)
			op(r,request)
			
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
			id = request.POST.get('id','')
			if id:
				r = Company.objects.filter(account=account.strip()).exclude(id=int(id))
			else:	
				r = Company.objects.filter(account=account.strip())
			if r.exists():
				return JsonResponse({'valid': False})

			return JsonResponse({'valid': True})

		elif action == 'export':
			if companys:
				e = xlwt.Workbook(encoding='utf-8')
				w = e.add_sheet(u'商家管理')
				w.write(0,0,'商家名称')
				w.write(0,1,'商家地址')
				w.write(0,2,'登陆账号')
				w.write(0,3,'联系人姓名')
				w.write(0,4,'联系人电话')
				w.write(0,5,'余额')
				w.write(0,6,'时长')
				w.write(0,7,'限制类型')
				w.write(0,8,'限制规则')
				w.write(0,9,'限制张数')
				w.write(0,10,'商家描述')
				w.write(0,11,'所属停车场')
				w.write(0,12,'状态')
				row = 1
				for i  in companys:
					w.write(row, 0, i.name)
					w.write(row, 1, i.address)
					w.write(row, 2, i.account)
					w.write(row, 3, i.owner)
					w.write(row, 4, i.phone)
					w.write(row, 5, i.balance)
					w.write(row, 6, i.duration)
					w.write(row, 7, i.get_type_display())
					w.write(row, 8, i.rule)
					w.write(row, 9, i.amount)
					w.write(row, 10, i.descript)
					w.write(row, 11,i.parkinglot.name if i.parkinglot else '')
					w.write(row, 12, i.get_status_display())
					row +=1
				output = io.BytesIO()
				e.save(output)
				# 重新定位到开始
				output.seek(0)
				response = HttpResponse(content_type='application/vnd.ms-excel')
				response['Content-Disposition'] = 'attachment;filename=company.xls'
				response.write(output.getvalue())
				return response

		elif action == 'select':
			name = request.POST.get('busi_name','')
			ass_name = request.POST.get('associate_name','')
			if name:
				name=int(name)
				companys = companys.filter(id=name).all()
				ctx['b']=name
			if ass_name:
				companys = companys.filter(owner__icontains=ass_name).all()
				ctx['a']=ass_name

	ctx['objects'] = ctx['company'] = companys
	ctx['parkinglot'] = ParkingLot.objects.filter(status=0)

	return (ctx,'company.html')