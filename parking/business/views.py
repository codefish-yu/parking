from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ApplyRecord

# Create your views here.

def com_login(request):
	ctx={}


	return render(request,'com_login.html',ctx)


def apply(request):
	ctx = {}

	return render(request,'apply.html',ctx)

@csrf_exempt
def grant(request):
	ctx = {}
	p=0
	records = ApplyRecord.objects.filter(status=0).all()


	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'change':
			p = int(request.POST.get('p'))

	ctx['p']=p
	ctx['records'] = records
	return render(request,'grant.html',ctx) 
