from django.shortcuts import render

# Create your views here.


def manage_login(request):
	ctx = {}

	return render(request,'manage_login.html',ctx)