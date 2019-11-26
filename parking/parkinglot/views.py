from django.shortcuts import render

# Create your views here.


'''停车场管理模块'''


def parking_lot(request):
	ctx = {'menu': 'parkinglot'}
	
	return render(request, 'parking_lot.html', ctx)