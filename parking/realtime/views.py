from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import * 
from parkinglot.models import *
from administrator.decorators import page, _save_attr_


import json
import base64
import datetime


'''实时管理模块'''


@csrf_exempt
def parkin(request):
    
    result = {
            'error_num': 0,
            'error_str': 'error info',
            # 'gpio_data': [{'action': 'on', 'ionum': 'io1'}],
            # 'passwd': 'xxxxxxx',
            # 'rs485_data': [{'data': 'AA55016400260009010002004343434343C5F0AF',
            #                  'encodetype': 'hex2string'},
            #                 {'data': 'AA551F6400220009D4C1423132333435012AA6AF'},
            #                 {'data': 'qlUBZAAmAAkBAAIAQ0NDQ0PF8K8=',
            #                  'encodetype': 'base64'}],
            # 'triger_data': {'action': 'on'},
            # 'whitelist_data': []
        }
    
    
    params = get_params(request)

    if 'type'in params and params['type'] == 'HeartBeat':

        pass
        
    if 'type'in params and params['type'] == 'online':
        print(params.keys())

        r = InAndOut(
            number=params['car_plate'],
            color=params['color'],
            logo=params['car_logo'],
            start_time=datetime.datetime.fromtimestamp(int(params['start_time'])),
            park_id=params['park_id'],
            cam_id=params['camera_id'],
            )


        park_id = params['park_id']
        parkinglot = ParkingLot.objects.filter(id=park_id)
        if parkinglot.exists():
            r.parkinglot = parkinglot.first()

        camera_id = params['camera_id']
        print(camera_id)
        camera = Camera.objects.filter(mac_address=camera_id)
        if camera.exists():
            print(camera.first())
            r.camera = camera.first()
            print(r.camera.in_or_out)
            if r.camera.in_or_out == 1:
                print('ssss')
            result["gpio_data"] = [{"ionum":"io1","action":"on"}]
            result["triger_data"] = {"action":"on"}
        try:
            picture =  base64.b64decode(params['picture'].replace('-', '+').replace('.', '=').replace('_','/'))
            plate_pic =  base64.b64decode(params['closeup_pic'].replace('-', '+').replace('.', '=').replace('_','/'))

            name = random_name()

            car = '/Users/dsc/Githome/parking/parking/media/car/' + name + '.jpg'
            plate = '/Users/dsc/Githome/parking/parking/media/plate/' + name + '.jpg'

            with open(car, 'wb') as f:
                f.write(picture)

            with open(plate, 'wb') as f:
                f.write(plate_pic)


            r.picture = 'car/' + name + '.jpg'
            r.closeup_pic = 'plate/' + name + '.jpg'

        except Exception as e:
            print(e)

        r.save()
    print(result)
    return JsonResponse(result)


def get_params(request):
    data = request.body.decode()

    params = {}
    for _ in data.split('&'):
        key = _.split('=')[0]
        val = _.replace(key+'=', '')
        params[key] = val
    
    return params


def random_name():
    import time 
    return str(time.time()).replace('.', '')


def parkout(request):
    pass


@csrf_exempt
@page
def in_out(request):
    '''出入场管理'''

    ctx = {}

    records = InAndOut.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'search':
            ctx['brand'] = brand = request.POST.get('brand', '')
            ctx['manufacturer'] = manufacturer = request.POST.get('manufacturer', '')
           
            gate_id = request.POST.get('gate_id', '')
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                records = records.filter(parkinglot_id=int(parkinglot_id))
                ctx['gates'] = Gate.objects.filter(parkinglot_id=int(parkinglot_id))
            if gate_id:
                ctx['gate_id'] = int(gate_id)
                records = records.filter(gate_id=int(gate_id))
            if brand:
                records = records.filter(brand=brand)
            if manufacturer:
                records = records.filter(manufacturer=manufacturer)
                

    ctx['objects'] = records.order_by('-start_time')
    # ctx['parkinglots'] = ParkingLot.objects.filter(status=0).all()
    # print(ctx['parkinglots'])
    # all_gates = {}

    # gates = Gate.objects.select_related('parkinglot').filter(parkinglot__status=0).order_by('parkinglot')
    # for i in gates:
    #     if i.parkinglot.id in all_gates:
    #         all_gates[i.parkinglot.id].append({'gate_id': i.id, 'gate_name': i.monitor})
    #     else:
    #         all_gates[i.parkinglot.id] = [{'gate_id': i.id, 'gate_name': i.monitor}]
    # ctx['all_gates'] = all_gates

    return (ctx, 'in_out.html')



