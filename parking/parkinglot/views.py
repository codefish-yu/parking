from django.shortcuts import render
from administrator import views as a
from .models import *

# Create your views here.


'''停车场管理模块'''


def parking_lot(request):
	ctx = {'menu': 'parkinglot'}

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'add':

			r = ParkingLot()
			a._save_attr_(r, request)
		elif action == 'update':
			id = request.POST.get('id', '')
			r = ParkingLot.objects.filter(id=id)
			a._save_attr_(r.first(), request)

		elif action == 'delete':
			ids = request.POST.getlist('ids', '')
			u = ParkingLot.objects.filter(id__in=ids).all()
			for item in u:
				item.status = -1
				item.save()

	ctx['parkinglot'] = parkinglot = ParkingLot.objects.filter(status=0).all()
	
	return render(request, 'parking_lot.html', ctx)
