from django.shortcuts import render

# Create your views here.


'''车辆管理模块'''


def inner_car(request):
	ctx = {'menu': 'car'}
	
	return render(request, 'inner_car.html', ctx)