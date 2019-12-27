from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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


	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'change':
			p = int(request.POST.get('p'))

	ctx['p']=p
	return render(request,'grant.html',ctx) 
