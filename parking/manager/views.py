from django.shortcuts import render

# Create your views here.


def manage_login(request):
	ctx = {}

	return render(request,'manage_login.html',ctx)


def manage_home(request):
	ctx = {}

	return render(request,'manage_home.html',ctx)