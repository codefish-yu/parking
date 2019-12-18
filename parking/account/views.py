from django.shortcuts import render
from administrator.decorators import *
from realtime.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from chargerule.models import *
from wechat.views import user_required 

# Create your views here.
@csrf_exempt
# @user_required
def spec_pass(request):
	ctx ={}
	
	records = InAndOut.objects.order_by('-update_time').all()
	record = records.first()
	p = 0

	def check_type(number):
		card = Card.objects.filter(car_number=number).first()
		if card:
			now = datetime.datetime.now()
			if now.day >= card.valid_start.day and now.day <=  card.valid_end.day:
				return 1,card
		return 0,None


	if request.method == 'POST':
		action =request.POST.get('action','')

		if action == 'check':
			
			today = datetime.datetime.now()
			if  record.in_time.day == today.day  or record.out_time.day == today.day or record.update_time.day == today.day:
				record = records.first()
				ctx['tip'] = 1 if record.out_time else 0

		elif action == 'pass':
			r_id = request.POST.get('id','')
			remark = request.POST.get('remark','')
			record = InAndOut.objects.filter(id=r_id).first()
			record.remark = remark
			record.save()

		elif action == 'in':
			records = records.filter(out_time=None).all()
			record = records.first()
			p=1

		elif action == 'out':
			records = InAndOut.objects.order_by('-update_time').all()
			record = records.first()
			p = 0


	ctx['p'] = p
	ctx['type'],ctx['card'] = check_type(record.number) if record else 0,0
	ctx['record'] = record
	ctx['records'] = records
	return render(request,'spec_pass.html',ctx)


@csrf_exempt
def correct(request):
	ctx = {}
	p = 0	

	record = InAndOut.objects.order_by('-update_time').first()

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'correct':
			number = ''
			for i in range(1,9):
				num = request.POST.get('num_'+str(i),'')
				number +=num
			record.number = number
			record.save()

		elif action == 'in':
			p=1

		elif action == 'out':
			p = 0

	ctx['p'] = p
	ctx['record'] = record
	return render(request,'correct.html',ctx)


def home(request):
	ctx = {}


	return render(request,'home.html',ctx)


def worker_login(request):
	ctx = {}
	

	return render(request,'worker_login.html',ctx)


# @user_required
@csrf_exempt
def record(request):
	ctx = {}
	records = InAndOut.objects.order_by('-update_time').all()
	tip = 0
	p=0

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

		elif action == 'in':
			records = records.filter(out_time=None).all()
			p=1

		elif action == 'out':
			records = InAndOut.objects.order_by('-update_time').all()
			p = 0
		
	ctx['p'] = p
	ctx['tip'] =tip
	ctx['records'] = records
	return render(request,'record.html',ctx)

# @user_required
def personal(request):
	ctx = {}
	

	return render(request,'personal.html',ctx)









