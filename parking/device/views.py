from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from administrator.decorators import page, _save_attr_

 
'''设备管理模块'''


@csrf_exempt
@page
def camera(request):
    '''摄像头管理'''

    ctx = {}

    cameras = Camera.objects.select_related('parkinglot','gate').all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Camera()            
            _save_attr_(r, request)

            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Camera.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()
            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()
        elif action == 'search':
            ctx['brand'] = brand = request.POST.get('brand', '')
            ctx['manufacturer'] = manufacturer = request.POST.get('manufacturer', '')
           
            gate_id = request.POST.get('gate_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                cameras = cameras.filter(parkinglot_id=int(parkinglot_id))
                ctx['gates'] = Gate.objects.filter(parkinglot_id=int(parkinglot_id))
            if gate_id:
                ctx['gate_id'] = int(gate_id)
                cameras = cameras.filter(gate_id=int(gate_id))
            if brand:
                cameras = cameras.filter(brand=brand)
            if manufacturer:
                cameras = cameras.filter(manufacturer=manufacturer)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Camera.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Camera.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action == 'get_gate':
            id = request.POST.get('id', '')
            gates = Gate.objects.filter(parkinglot_id=id)
            gates = [{'name': _.name, 'id':_.id} for _ in gates]
            return JsonResponse({'success':True, 'result': gates})

    ctx['objects'] = cameras.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    print(ctx['parkinglots'])
    all_gates = {}

    gates = Gate.objects.select_related('parkinglot').filter(parkinglot__status=0).order_by('parkinglot')
    for i in gates:
        if i.parkinglot.id in all_gates:
            all_gates[i.parkinglot.id].append({'gate_id': i.id, 'gate_name': i.name if i.name else ''})
        else:
            all_gates[i.parkinglot.id] = [{'gate_id': i.id, 'gate_name': i.name if i.name else ''}]
    ctx['all_gates'] = all_gates
    print(all_gates)

    return (ctx, 'camera.html')


@csrf_exempt
@page
def brake(request):
    '''闸机管理'''

    ctx = {}

    brakes = Brake.objects.select_related('parkinglot','gate').all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Brake()            
            _save_attr_(r, request)

            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Brake.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()
            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()
        elif action == 'search':
            ctx['brand'] = brand = request.POST.get('brand', '')
            ctx['manufacturer'] = manufacturer = request.POST.get('manufacturer', '')
           
            gate_id = request.POST.get('gate_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                brakes = brakes.filter(parkinglot_id=int(parkinglot_id))
                ctx['gates'] = Gate.objects.filter(parkinglot_id=int(parkinglot_id))
            if gate_id:
                ctx['gate_id'] = int(gate_id)
                brakes = brakes.filter(gate_id=int(gate_id))
            if brand:
                brakes = brakes.filter(brand=brand)
            if manufacturer:
                brakes = brakes.filter(manufacturer=manufacturer)
                
        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Brake.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Brake.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action == 'get_gate':
            id = request.POST.get('id', '')
            gates = Gate.objects.filter(parkinglot_id=id)
            gates = [{'name': _.name, 'id':_.id} for _ in gates]
            return JsonResponse({'success':True, 'result': gates})

    ctx['objects'] = brakes.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    print(ctx['parkinglots'])
    all_gates = {}

    gates = Gate.objects.select_related('parkinglot').filter(parkinglot__status=0).order_by('parkinglot')
    for i in gates:
        if i.parkinglot.id in all_gates:
            all_gates[i.parkinglot.id].append({'gate_id': i.id, 'gate_name': i.monitor})
        else:
            all_gates[i.parkinglot.id] = [{'gate_id': i.id, 'gate_name': i.monitor}]
    ctx['all_gates'] = all_gates

    return (ctx, 'brake.html')


@csrf_exempt
@page
def groundsensor(request):
    '''地感管理'''

    ctx = {}

    groundsensors = GroundSensor.objects.select_related('parkinglot','gate').all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = GroundSensor()            
            _save_attr_(r, request)

            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()

            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()

        elif action == 'update':
            id = request.POST.get('id', '')

            r = GroundSensor.objects.filter(id=id).first()
            _save_attr_(r, request)
            parkinglot_id = request.POST.get('parkinglot_id', '')
            if parkinglot_id:
                p = ParkingLot.objects.filter(id=parkinglot_id).first()
                if p: 
                    r.parkinglot = p
                    r.save()
            gate_id = request.POST.get('gate_id', '')
            if gate_id:
                p = Gate.objects.filter(id=gate_id).first()
                if p: 
                    r.gate = p
                    r.save()
        elif action == 'search':
            ctx['brand'] = brand = request.POST.get('brand', '')
            ctx['manufacturer'] = manufacturer = request.POST.get('manufacturer', '')
           
            gate_id = request.POST.get('gate_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                groundSensors = groundsensors.filter(parkinglot_id=int(parkinglot_id))
                ctx['gates'] = Gate.objects.filter(parkinglot_id=int(parkinglot_id))
            if gate_id:
                ctx['gate_id'] = int(gate_id)
                groundsensors = groundsensors.filter(gate_id=int(gate_id))
            if brand:
                groundsensors = groundsensors.filter(brand=brand)
            if manufacturer:
                groundsensors = groundsensors.filter(manufacturer=manufacturer)
                
        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            GroundSensor.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = GroundSensor.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action == 'get_gate':
            id = request.POST.get('id', '')
            gates = Gate.objects.filter(parkinglot_id=id)
            gates = [{'name': _.name, 'id':_.id} for _ in gates]
            return JsonResponse({'success':True, 'result': gates})

    ctx['objects'] = groundsensors.order_by('-buy_time')
    ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    print(ctx['parkinglots'])
    all_gates = {}

    gates = Gate.objects.select_related('parkinglot').filter(parkinglot__status=0).order_by('parkinglot')
    for i in gates:
        if i.parkinglot.id in all_gates:
            all_gates[i.parkinglot.id].append({'gate_id': i.id, 'gate_name': i.monitor})
        else:
            all_gates[i.parkinglot.id] = [{'gate_id': i.id, 'gate_name': i.monitor}]
    ctx['all_gates'] = all_gates

    return (ctx, 'groundsensor.html')
