from django.shortcuts import render

# Create your views here.

def com_login(request):
	ctx={}


	return render(request,'com_login.html',ctx)


def apply(request):
	ctx = {}

	return render(request,'apply.html',ctx)


def grant(request):
	ctx = {}

	return render(request,'grant.html',ctx) 
