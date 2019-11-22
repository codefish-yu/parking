from django.shortcuts import render

# Create your views here.


'''系统设置模块'''


def login(request):

	if request == 'POST':
		pass

		return render(request, 'base.html')

	return render(request, 'login.html')


def base(request):
	return render(request, 'base.html')


def skin(request):
	return render(request, 'skin.html')
	

def index(request):
	ctx = { 'menu': 'index'}
	
	return render(request, 'index.html', ctx)