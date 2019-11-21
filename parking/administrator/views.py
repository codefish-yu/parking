from django.shortcuts import render

# Create your views here.


def index(request):
	ctx = { 'menu': 'index'}
	
	return render(request, 'index.html', ctx)