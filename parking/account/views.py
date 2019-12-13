from django.shortcuts import render
from administrator.decorators import *

# Create your views here.
def spec_pass(request):
	ctx ={}

	
	return render(request,'spec_pass.html',ctx)



def correct(request):
	ctx = {}

	
	return render(request,'correct.html',ctx)


def home(request):
	ctx = {}


	return render(request,'home.html',ctx)


def worker_login(request):
	ctx = {}
	

	return render(request,'worker_login.html',ctx)

