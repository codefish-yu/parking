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
    # resp = {
    #     'type': 'online', 
    #     'mode': '5', 
    #     'plate_num': '京PH3XJ0', 
    #     'car_logo': '未知', 
    #     'plate_val': 'true', 
    #     'confidence': '24', 
    #     'plate_color': '蓝色', 
    #     'car_color': '未知', 
    #     'vehicle_type': '轿车', 
    #     'start_time': '1575536095', 
    #     'park_id': '5', 
    #     'cam_id': '100200041313', 
    #     'cam_ip': '192.168.10.100', 
    #     'vdc_type': 'in', 
    #     'is_whitelist': 'false', 
    #     'triger_type': 'video'
    # }

    params = get_params(request)
    print(params)
    if 'type'in params and params['type'] == 'HeartBeat':
        print(params.keys())

        pass
        
    if 'type'in params and params['type'] == 'online':
        print(params.keys())

        if params['vdc_type'] == 'in':  # 入场
            r = InAndOut(
                number=params['plate_num'],
                in_time=datetime.datetime.fromtimestamp(int(params['start_time'])),
                plate_color_in=params['plate_color'],
                logo_in=params['car_logo'],
                park_id=params['park_id'],
                cam_id_in=params['cam_id'],
                cam_ip_in=params['cam_ip'],
                plate_val_in=True if params['plate_val'] == 'true' else False,
                confidence_in=params['confidence'],
                color_in=params['car_color'],
                vdc_type=params['vdc_type'],
                triger_type_in=params['triger_type'],
                vehicle_type_in=params['vehicle_type'],
            )

        else:  # 出场
            number = params['plate_num']
            print(number)
            r = InAndOut.objects.filter(number=number).order_by('-in_time').first()

            if r:
                r.out_time = datetime.datetime.fromtimestamp(int(params['start_time']))
                r.plate_color_out = params['plate_color']
                r.logo_out = params['car_logo']
                r.park_id = params['park_id']
                r.cam_id_out = params['cam_id']
                r.cam_ip_out = params['cam_ip']
                r.plate_val_out = True if params['plate_val'] == 'true' else False
                r.confidence_out = params['confidence']
                r.color_out = params['car_color']
                r.vdc_type = params['vdc_type']
                r.triger_type_out = params['triger_type']
                r.vehicle_type_out = params['vehicle_type']

            if r.bill and r.bill.status == 1:
                print('sss')
                result["gpio_data"] = [{"ionum":"io1","action":"on"}] # 开闸
            else:
                b = Bill(
                    payable=100, 
                    payment=100, 
                    pay_time=datetime.datetime.now(),
                    status=0
                )
                b.save()
                r.bill = b
        
        park_id = params['park_id']
        parkinglot = ParkingLot.objects.filter(id=park_id)
        if parkinglot.exists():
            r.parkinglot = parkinglot.first()
            
        camera_id = params['cam_id']
        camera = Camera.objects.filter(mac_address=camera_id)
        if camera.exists():
                         
            if params['vdc_type'] == 'in':
                r.camera_in = camera.first()
                r.cam_id_in = camera_id
            else:
                r.camera_out = camera.first()
                r.cam_id_out = camera_id

            if not r.parkinglot and r.camera_in.parkinglot:
                r.parkinglot = r.camera_in.parkinglot
          
        # 保存汽车出入时抓拍的全景图和车牌特写图
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

            if params['vdc_type'] == 'in':
                r.picture_in = 'car/' + name + '.jpg'
                r.closeup_pic_in = 'plate/' + name + '.jpg'
            else:
                r.picture_out = 'car/' + name + '.jpg'
                r.closeup_pic_out = 'plate/' + name + '.jpg'

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
            parkinglot_id = request.POST.get('parkinglot_id', '')

            if parkinglot_id:
                ctx['parkinglot_id'] = int(parkinglot_id)
                records = records.filter(parkinglot_id=int(parkinglot_id))
        elif action == 'pay':
            id = request.POST.get('id', '')
            if id:
                r = InAndOut.objects.filter(id=id).first()
                if r:
                    if r.bill:
                        r.bill.status = 1
                        r.bill.save()
                    else:
                        b = Bill(
                            payable=100, 
                            payment=100, 
                            pay_time=datetime.datetime.now(),
                            status=1
                        )
                        b.save()
                        r.bill = b
                        r.save()

                    return JsonResponse({'success': True})

            return JsonResponse({'success': False})

    ctx['objects'] = records.order_by('-update_time')
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

@page
def pay(request):

    ctx = {}
    pays = Pay.objects.all()

    if request.method == 'POST':
        action = request.POST.get(action,'')

        if action == 'select':
            p = request.POST.get('parkinglot','')
            u = request.POST,get('tollman','')
            t = request.POST.get('type','','')
            s = request.POST.get('start_time','')
            e = request.POST.get('end_time','')

            ctx['p'] = p
            ctx['t'] = t
            ctx['u'] = u
            ctx['s'] = s
            ctx['e'] = e

    ctx['objects'] = ctx['pays'] = pays
    return (ctx,'pay.html')


