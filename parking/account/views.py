from django.shortcuts import render,redirect
from administrator.decorators import *
from realtime.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from chargerule.models import *
from account.models import *
from meta.models import User,WechatUser
from meta import api
import functools

# Create your views here.

def user_required(func):

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        from meta import api
        
        wrapper.__name__ = func.__name__

        token = request.session['token'] if 'token' in request.session else ''
        
        if not token:
            token = request.GET.get('token', '')
            if token:
                request.session['token'] = token

        next_url = request.get_full_path()

        if not token:
            return redirect('/login/public/account/?next=' + next_url)

        try:
            user = api.check_token(token)
        except APIError:
            return redirect('/login/public/account/?next=' + next_url)

        request.user = user
        result = func(request, user=user, *args, **kwargs)
        return result

    return wrapper


@csrf_exempt
# @user_required
def spec_pass(request):
	ctx ={}
	user = User.objects.first()
	records = InAndOut.objects.order_by('-update_time').all()
	record = records.first()
	p = 0

	def check_type(number):
		card = Card.objects.filter(car_number=number).first()
		if card:
			now = datetime.datetime.now()
			if now.day >= card.valid_start.day and now.day <=  card.valid_end.day:
				return 1,card
		return [0,None]


	if request.method == 'POST':
		action =request.POST.get('action','')

		if action == 'check':
			record = InAndOut.objects.order_by('-update_time').first()
			exc = ExceptRecord.objects.order_by('-time').first()
			if record.update_time < exc.time:
				record = exc

				return redirect('/account/correct/')

			today = datetime.datetime.now()
			if  record.update_time.day == today.day:
				p= 0 if record.out_time else 1
				

		elif action == 'pass':
			r_id = request.POST.get('id','')
			remark = request.POST.get('remark','')
			record = InAndOut.objects.filter(id=r_id).first()
			record.remark = remark
			record.save()

			# 操作员放行记录
			r = SpecRecord()
			r.tollman = user
			r.record = record
			r.save()

			# 修改放行参数
			chek = SpecRecord.objects.filter(tollman=user,record__is_spec=1).all()
			re = WorkRecord.objects.filter(worker=user).order_by('-time').first()
			re.spec_num = len(chek)
			re.save()

		elif action == 'in':
			records = records.filter(out_time=None).all()
			record = records.first()
			p=1

		elif action == 'out':
			records = InAndOut.objects.order_by('-update_time').all()
			record = records.first()
			p = 0


	ctx['p'] = p
	ctx['type'],ctx['card'] = check_type(record.number) if record else [0,0]
	ctx['record'] = record
	ctx['records'] = records
	return render(request,'spec_pass.html',ctx)


@csrf_exempt
def correct(request):
	ctx = {}
	record = ExceptRecord.objects.order_by('-time').first()
	p = record.direction if record else 0

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'correct':
			number = ''
			for i in range(1,9):
				num = request.POST.get('num_'+str(i),'')
				number +=num
			
			r = InAndOut.objects.filter(number=number).first()
			if r:
				r.final_out_time = record.time
				r.plate_color_out = reccord.plate_color
				r.logo_out = record.logo
				r.park_id = record.park_id
				r.cam_id_out = record.cam_id
				r.cam_ip_out = record.cam_ip
				r.plate_val_out = record.plate_val
				r.confidence_out = record.confidence
				r.color_out = record.color
				r.vdc_type = record.vdc_type
				r.triger_type_out = record.triger_type
				r.vehicle_type_out = record.vehicle_type
				r.camera_out = record.camera
				r.picture = record.picture
				r.closeup_pic = record.closeup_pic
				r.exception = 1
				r.save()
				record = r

		elif action == 'in':
			p=1
			record = ExceptRecord.order_by.filter(direction=p).first()
			

		elif action == 'out':
			p = 0
			record = ExceptRecord.order_by.filter(direction=p).first()


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

	def transfor(t):
		return datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')

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
			records = InAndOut.objects.filter(out_time=None).order_by('-update_time').all()
			p=1

		elif action == 'out':
			records = InAndOut.objects.order_by('-update_time').all()
			p = 0
		elif action == 'ex':
			records = []
			p=2

		elif action == 'select':
			start = request.POST.get('start','')
			end = request.POST.get('end','')
			if start:
				ctx['start'] =start
				start = transfor(start+' 00:00:00')
				if p:
					records = records.filter(in_time__gte=start).all()
				else:
					records = records.filter(out_time__gte=start).all()

			if end:
				ctx['end'] = end
				end = transfor(end+' 00:00:00')
				if p:
					records = records.filter(in_time__lte=end).all()
				else:
					records = records.filter(out_time__lte=end).all()

		
	ctx['p'] = p
	ctx['tip'] =tip
	ctx['records'] = records
	return render(request,'record.html',ctx)

# @user_required
@csrf_exempt
def personal(request):
	ctx = {}

	def get_time(time):
		return time.hour+time.minute/60

	def get_duration(r):
		now = datetime.datetime.now()
		if not r.offline:
			r.duration = get_time(now)-get_time(r.time)
		else:
			r.duration += get_time(now)-get_time(r.offline)

		r.offline = now
		r.save()
	
	user = User.objects.first()
	worker = Worker.objects.filter(user=user).first()
	workrecord = WorkRecord.objects.filter(worker=user).first()
	get_duration(workrecord)


	if request.method == 'POST':
		action =request.POST.get('action','')
		if action == 'offline':

			get_duration(workrecord)
			return redirect('/account/begin_work')

	ctx['parkinglot']=worker.parkinglot.name
	ctx['record'] = workrecord	
	ctx['wuser'] = WechatUser.objects.filter(user=user).first()
	return render(request,'personal.html',ctx)

@csrf_exempt
def begin_work(request):
	ctx = {}
	user = User.objects.first()

	def set_work(user,p,g):
		today = datetime.datetime.now()
		rs = WorkRecord.objects.order_by('-time').first()
		p = ParkingLot.objects.filter(id=int(p)).first()
		g = Gate.objects.filter(id=int(g)).first()
		if today.day != rs.time.day:
			r = WorkRecord()
			r.worker = user
			r.time = datetime.datetime.now()
			r.parkinglot = p
			r.gate = g
		else:
			r = WorkRecord.objects.filter(worker=user).order_by('-time').first()
			r.offline = datetime.datetime.now()

		r.save()

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'login':
			parkinglot = request.POST.get('parkinglot','')
			gate = request.POST.get('gate','')
			set_work(user,parkinglot,gate)



	return render(request,'begin_work.html',ctx)









