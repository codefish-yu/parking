from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from administrator.decorators import page, _save_attr_
'''停车场管理模块'''


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

	ctx['parkinglot'] = parkinglot = ParkingLot.objects.filter(status=0).all()
	
	return render(request, 'parking_lot.html', ctx)


def gate(request):
	ctx = {}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = Gate()
			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Gate.objects.filter(id=id)
			_save_attr_(r.first(), request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Gate.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

	ctx['gates'] = gate = Gate.objects.filter(status=0).all()

	return render(request,'gate.html',ctx)


@page
def worker(request):
    ''' 车场员工 ''' 
    
    ctx = {}

    workers = Worker.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Worker()
            _save_attr_(r, request)


        elif action == 'update':
            id = request.POST.get('id', '')

            r = Worker.objects.filter(id=id).first()
            _save_attr_(r, request)
            save_auth(r, request)

        elif action == 'search':
            ctx['worker_name'] = worker_name = request.POST.get('worker_name', '')
            roles = Worker.objects.filter(worker_name__contains=worker_name.strip())

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).delete()

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

    return render(ctx, 'worker.html')


def zone(request):
	ctx ={}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = Zone()
			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Zone.objects.filter(id=id)
			_save_attr_(r.first(), request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Zone.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

	ctx['zone'] = Zone.objects.filter(status=0).all()

	return render(request,'zone.html',ctx)



def place(request):

	ctx ={}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = Place()
			_save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = Place.objects.filter(id=id)
			_save_attr_(r.first(), request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = Place.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

		# elif action == 'select':

	ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
	ctx['zones'] = Zone.objects.filter(status=0).all()
	ctx['place'] = Place.objects.filter(status=0).all()

	return render(request,'place.html',ctx)







