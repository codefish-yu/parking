from django.shortcuts import render
from administrator.decorators import *
from realtime.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from chargerule.models import *

# Create your views here.
@csrf_exempt
def spec_pass(request):
	ctx ={}
	
	records = InAndOut.objects.order_by('-update_time').all()
	record = records.first()

	def check_type(number):
		card = Card.objects.filter(car_number=number).first()
		if card:
			now = datetime.datetime.now()
			if now.day >= card.valid_start.day and now.day <=  card.valid_end.day:
				return 1
		return 0


	if request.method == 'POST':
		action =request.POST.get('action','')

		if action == 'check':
			
			today = datetime.datetime.now()
			if  record.in_time.day == today.day  or record.out_time.day == today.day or record.update_time.day == today.day:
				record = records.first()
				ctx['tip'] = 1 if record.out_time else 0


	ctx['type'] = check_type(record.number)
	ctx['record'] = record
	ctx['records'] = records
	return render(request,'spec_pass.html',ctx)



def correct(request):
	ctx = {}	

	record = InAndOut.objects.order_by('-update_time').first()

	if action == 'correct':
		pass

	ctx['record'] = record
	return render(request,'correct.html',ctx)


def home(request):
	ctx = {}


	return render(request,'home.html',ctx)


def worker_login(request):
	ctx = {}
	

	return render(request,'worker_login.html',ctx)



def record(request):
	ctx = {}
	records = InAndOut.objects.order_by('-update_time').all()
	tip = 0

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'change':
			status = request.POST.get('status','')
			if not int(status):
				records = records.filter(is_spec=1).all()
				tip = 1
			else:
				records = InAndOut.objects.order_by('-update_time').all()
				tip = 0

	ctx['tip'] =tip
	ctx['records'] = records
	return render(request,'record.html',ctx)


def personal(request):
	ctx = {}
	

	return render(request,'personal.html',ctx)









