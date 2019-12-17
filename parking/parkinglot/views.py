from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from administrator.decorators import page, _save_attr_
from meta.qrcode import make_qrcode
'''停车场管理模块'''

# 停车场管理
@page
def parking_lot(request):

	ctx = {'menu': 'parkinglot'}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = ParkingLot()
			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = ParkingLot.objects.filter(id=id)
			_save_attr_(r.first(), request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = ParkingLot.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

	ctx['parkinglot'] = ctx['objects'] = ParkingLot.objects.filter(status=0).all()
	
	return (ctx, 'parking_lot.html')

# 出入口管理
@page
def gate(request):
	ctx = {}
	gate = Gate.objects.filter(status=0).all()

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':
			r = Gate()
			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()
			_save_attr_(r, request)
			t = request.POST.get('use_type','')
			if t:
				t=int(t)
			if t == 1:
				url = 'http://parking.metatype.cn/wechat/parkin/'+str(r.parkinglot.id)+'/'+str(r.id)+'/'
			elif t==2:
				url = 'http://parking.metatype.cn/wechat/parkout/'+str(r.parkinglot.id)+'/'+str(r.id)+'/'
			elif t == 0:
				url = 'http://parking.metatype.cn/wechat/parkout/'+str(r.parkinglot.id)+'/'
			c_name = 'code_'+str(r.parkinglot.id)+'_'+str(r.id)+'_'+str(t)	
			r.code = make_qrcode(url,c_name+'.png')
			r.save()
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Gate.objects.filter(id=id).first()
			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()

			_save_attr_(r, request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Gate.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()
		elif action == 'select':
			use_type = request.POST.get('use_type')
			if use_type:
				gate = Gate.objects.filter(use_type=use_type,status=0).all()
				ctx['tip'] = use_type

		elif action == 'barcode':
			pass

	ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
	ctx['gates'] = ctx['objects'] = gate 

	return (ctx,'gate.html')

@csrf_exempt
@page
def worker(request):
    ''' 车场员工 ''' 
    
    ctx = {}

    workers = Worker.objects.all().filter(is_delete=0)

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Worker()            
            _save_attr_(r, request)

            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Worker.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

        elif action == 'search':
            ctx['name'] = name = request.POST.get('name', '')
            ctx['number'] = number = request.POST.get('number', '')
            forbidden = request.POST.get('forbidden', '')
            parkinglot = request.POST.get('parkinglot', '')

            if forbidden:
                ctx['forbidden'] = int(forbidden)
                workers = workers.filter(forbidden=int(forbidden))
            if parkinglot:
                ctx['parkinglot'] = int(parkinglot)
                workers = workers.filter(parkinglot_id=int(parkinglot))
            if number:
                workers = workers.filter(number__contains=number)
            if name:
                workers = workers.filter(name__contains=name)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).update(is_delete=1)

        elif action == 'forbidden':
            id = request.POST.get('id', '')
            Worker.objects.filter(id=id).update(forbidden=1)
            return JsonResponse({'success': True})

        elif action == 'awaken':
            id = request.POST.get('id', '')
            Worker.objects.filter(id=id).update(forbidden=0)
            return JsonResponse({'success': True})

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Worker.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

    ctx['objects'] = workers
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()

    return (ctx, 'worker.html')

# 区域管理
@page
def zone(request):
	ctx ={}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = Zone()

			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()

			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Zone.objects.filter(id=id).first()

			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()

			_save_attr_(r, request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Zone.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

	ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
	ctx['zone'] = ctx['objects'] = Zone.objects.filter(status=0).all()

	return (ctx,'zone.html')


# 泊位管理
@page
@csrf_exempt
def place(request):

	ctx ={}
	place = Place.objects.filter(status=0).all()
	zone = Zone.objects.filter(status=0).all()

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = Place()

			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()

			zon = request.POST.get('zone')
			if zon:
				r.zone = Zone.objects.filter(id=int(zon)).first()
				r.save()

			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Place.objects.filter(id=id).first()

			park = request.POST.get('parkinglot')
			if park:
				r.parkinglot = ParkingLot.objects.filter(id=int(park)).first()
				r.save()

			zon = request.POST.get('zone')
			if zon:
				r.zone = Zone.objects.filter(id=int(zon)).first()
				r.save()

			_save_attr_(r, request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Place.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

		elif action == 'select':
			use_type = request.POST.get('use_type')
			car_type = request.POST.get('car_type')
			park = request.POST.get('parkinglot')
			zon = request.POST.get('zone')

			if use_type != '':
				place = place.filter(use_type=use_type)
			if car_type != '':
				place = place.filter(car_type=car_type)
			if park != '':
				place = place.filter(parkinglot__id=park)
			if zon != '':
				place = place.filter(zone__id=zon)

			ctx['u'] = use_type
			ctx['c'] = car_type
			ctx['p'] = park

		elif action == 'getZone':
			
			id = request.POST.get('id')
			zones = zone.filter(parkinglot__id=id).all()
			tmp =[]

			for i in zones:
				d = {
				'id':i.id,
				'name':i.zone_name
				}
				tmp.append(d)

			return JsonResponse({'data':tmp})

				
	ctx['zones'] = zone
	ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
	ctx['place'] = ctx['objects'] = place

	return (ctx,'place.html')







