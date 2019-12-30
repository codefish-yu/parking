from django.shortcuts import render,redirect
from administrator.decorators import *
from parkinglot.models import *
from realtime.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from chargerule.models import *
from account.models import *
from meta.models import User,WechatUser
from device.models import * 
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
        	# user = User.objects.first()
            return redirect('/login/public/account/?next=' + next_url)

        try:
            user = api.check_token(token)
        except APIError:

            return redirect('/login/public/account/?next=' + next_url)

        request.user = user
        result = func(request, user=user, *args, **kwargs)
        return result

    return wrapper


def max(a,b):
	if a.update_time>b.update_time:
		return a
	return b

def all_or_fir(obj,t=1):
	if t == 0:
		return obj.all()
	else:
		return obj.first()

def get_inandout(id,t=0,r=1):
	c = Camera.objects.filter(gate__id=id,in_or_out=0 if t else 1).first()
	if t == 1:
		return all_or_fir(InAndOut.objects.filter(camera_in=c,status__in=[-1,0]).order_by('-update_time'),r)
	elif t == 2:
		return all_or_fir(ExceptRecord.objects.filter(status=0).order_by('-update_time'),r)

	return all_or_fir(InAndOut.objects.filter(camera_out=c).exclude(status__in=[-1,0]).order_by('-update_time'),r)


def get_record(gate_id):
	ri = get_inandout(gate_id,1)
	ro = get_inandout(gate_id)
	exc =get_inandout(gate_id,2) 
	if not exc:
		return max(ri,ro)

	return max(exc,max(ri,ro))

def get_gate_id(user):
	wk = WorkRecord.objects.filter(worker=user).order_by('-time').first()

	return wk.gate.id


@csrf_exempt
@user_required
def spec_pass(request,user):
	ctx ={}
	gate_id = get_gate_id(user)
	record = get_inandout(gate_id)
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
			record = get_record(gate_id)
			if str(record._meta) == 'realtime.exceptrecord': 
			
				return redirect('/account/correct/')
			if not record.out_time:
				ctx['p'] = 1

			
		elif action == 'pass':
			r_id = request.POST.get('id','')
			remark = request.POST.get('remark','')
			audio = request.FILES.get('audio','')
			if r_id:
				record = InAndOut.objects.filter(id=r_id).first()
				record.is_spec = 1
				record.remark = remark
				record.save()

			# 操作员放行记录
			r = SpecRecord()
			r.tollman = user
			r.record = record
			r.audio = audio
			r.save()

			# 修改放行参数
			
			chek = SpecRecord.objects.filter(tollman=user,record__is_spec=1).all()
			re = WorkRecord.objects.filter(worker=user).order_by('-time').first()
			if re:
				re.spec_num = len(chek)
				re.save()

		elif action == 'in':
			record = get_inandout(gate_id,1)
			p=1

		elif action == 'out':
			record = get_inandout(gate_id,0)
			p = 0


	ctx['p'] = p
	ctx['type'],ctx['card'] = check_type(record.number) if record else [0,0]
	ctx['record'] = record
	return render(request,'spec_pass.html',ctx)


@user_required
@csrf_exempt
def correct(request,user):
	ctx = {}
	gate_id = get_gate_id(user)
	record = get_inandout(gate_id,2) 
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
			record = ExceptRecord.objects.filter(direction=p,status=0).order_by('-update_time').first()
			

		elif action == 'out':
			p = 0
			record = ExceptRecord.objects.filter(direction=p,status=1).order_by('-update_time').first()


	ctx['p'] = p
	ctx['record'] = record
	return render(request,'correct.html',ctx)


@user_required
@csrf_exempt
def record(request,user):
	
	def transfor(t):
		return datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')

	ctx = {}
	gate_id = get_gate_id(user)
	records = get_inandout(gate_id,0,0)
	tip = 0
	p=0

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'change':
			status = request.POST.get('status','')
			p = request.POST.get('ps','')
			p = int(p)
			records = get_inandout(gate_id,p,0)
			if not int(status):
				records = records.filter(is_spec=1).all()
				tip = 1
			else:
				tip = 0

		elif action == 'in':
			p=1
			records = get_inandout(gate_id,p,0)

		elif action == 'out':
			p = 0
			records = get_inandout(gate_id,p,0)

		elif action == 'ex':
			p=2
			records = get_inandout(gate_id,p,0)
			
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

	ctx['ex'] =len(get_inandout(gate_id,2,0))	
	ctx['p'] = p
	ctx['tip'] =tip
	ctx['records'] = records
	return render(request,'record.html',ctx)


@user_required
@csrf_exempt
def personal(request,user):
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
	
	worker = Worker.objects.filter(user=user).first()
	workrecord = WorkRecord.objects.filter(worker=user).order_by('-time').first()
	get_duration(workrecord)


	if request.method == 'POST':
		action =request.POST.get('action','')
		if action == 'offline':

			get_duration(workrecord)
			return redirect('/account/begin_work')

	ctx['parkinglot']=workrecord.parkinglot.name if workrecord.parkinglot else None
	ctx['record'] = workrecord	
	ctx['wuser'] = WechatUser.objects.filter(user=user).first()
	return render(request,'personal.html',ctx)


@user_required
@csrf_exempt
def begin_work(request,user):
	ctx = {}

	def serialize(obj):
		list = []
		for i in obj:
			d = {
				"id":i.id,
				"name":i.name
			}
			list.append(d)
		return list


	def set_wc(u,p,g):
		r = WorkRecord()
		r.worker = u
		r.time = datetime.datetime.now()
		r.parkinglot = p
		r.gate = g
		return r



	def set_work(us,p,g):
		today = datetime.datetime.now()
		rs = WorkRecord.objects.filter(worker=us).order_by('-time').first()
		p = ParkingLot.objects.filter(id=int(p)).first()
		g = Gate.objects.filter(id=int(g)).first()
		if not rs:
			r = set_wc(us,p,g)

		elif today.day != rs.time.day:
			r = set_wc(us,p,g)
		
		else:
			r = WorkRecord.objects.filter(worker=us).order_by('-time').first() 
			r.offline = datetime.datetime.now()

		r.save()

		

	if request.method == 'POST':
		action = request.POST.get('action','')
		if action == 'login':
			parkinglot = request.POST.get('parkinglot','')
			gate = request.POST.get('gate','')
			set_work(user,parkinglot,gate)

			return redirect('/account/spec_pass/')

		elif action == 'gate':
			p_id = request.POST.get('parkinglot','')
			gates = Gate.objects.filter(parkinglot__id=p_id,status=0).all()

			return JsonResponse({'data':serialize(gates)})


	ctx['parkinglots'] = ParkingLot.objects.all()
	return render(request,'begin_work.html',ctx)









