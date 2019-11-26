from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from administrator.decorators import page, _save_attr_
'''停车场管理模块'''


def parking_lot(request):
    
    ctx = {'menu': 'parkinglot'}

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':

            r = ParkingLot()
            _save_attr_(r, request)
        elif action == 'update':
            id = request.POST.get('id', '')
            r = ParkingLot.objects.filter(id=id)
            _save_attr_(r.first(), request)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = ParkingLot.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()

    ctx['parkinglot'] = parkinglot = ParkingLot.objects.filter(status=0).all()
    
    return render(request, 'parking_lot.html', ctx)



@page
def worker(request):
    ''' 车场员工 ''' 
    
    ctx = {}

    workers = Worker.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Worker()            
            _save_attr_(r, request)

            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Worker.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

        elif action == 'search':
            ctx['worker_name'] = worker_name = request.POST.get('worker_name', '')
            roles = Worker.objects.filter(worker_name__contains=worker_name.strip())

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).update(is_delete=1)

        elif action == 'forbidden':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).update(forbidden=1)

        elif action == 'awaken':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).update(forbidden=0)

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Worker.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

    ctx['objects'] = workers
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()

    return (ctx, 'worker.html')


