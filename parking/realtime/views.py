from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .models import * 
from parkinglot.models import *
from administrator.decorators import page, _save_attr_,export_excel,get_price


import json
import base64
import datetime
import io
import xlwt


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
        cam_id = params['cam_id']
        camera = Camera.objects.filter(mac_address=camera_id).first()
        if camera:
            if camera.gate:
                open_order = OpeningOrder.objects.filter(gate=camera.gate, status=2)
                if open_order.exists():
                    open_order.update(status=1)
                    result["gpio_data"] = [{"ionum":"io1","action":"on"}] # 开闸
        
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
            r = InAndOut.objects.filter(number=number, status=0).order_by('-in_time').first()

            if r:
                r.final_out_time = datetime.datetime.fromtimestamp(int(params['start_time']))
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
                    billable=100, 
                    billment=100, 
                    bill_time=datetime.datetime.now(),
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
                f.close()

            with open(plate, 'wb') as f:
                f.write(plate_pic)
                f.close()

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
        elif action == 'bill':
            id = request.POST.get('id', '')
            if id:
                r = InAndOut.objects.filter(id=id).first()
                if r:
                    if r.bill:
                        r.bill.status = 1
                        r.bill.save()
                    else:
                        b = Bill(
                            billable=100, 
                            billment=100, 
                            bill_time=datetime.datetime.now(),
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
def bill(request):

    ctx = {}
    bills = Bill.objects.all()

    def g_t(str):
        return datetime.datetime.strptime(str,'%Y-%m-%d %H:%M')

    if request.method == 'POST':
        action = request.POST.get('action','')

        if action == 'select':
            p = request.POST.get('parkinglot','')
            w = request.POST.get('tollman','')
            t = request.POST.get('type','')
            s = request.POST.get('in_time','')
            e = request.POST.get('out_time','')

            if p:
                tmp =[]    
                iao = InAndOut.objects.filter(parkinglot_id=p).all()
                for i in iao:
                    tmp.append(i.bill)

                bills =tmp
            if s:
                tmp =[] 
                start = g_t(s)
                iao = InAndOut.objects.filter(in_time__gt=start).all()
                for i in iao:
                    tmp.append(i.bill)

                bills =tmp
            if e:
                tmp =[] 
                end = g_t(e)
                iao = InAndOut.objects.filter(out_time__lt=end).all()
                for i in iao:
                    tmp.append(i.bill)

                bills =tmp

            if w:
                if isinstance(bills,list):
                    for i in bills:
                        if i.tollman:
                            if i.tollman.id !=int(q):
                                bills.remove(i)
                        else:
                            bills.remove(i)
                else:
                    bills = bills.filter(tollman__id=int(w)).all()
            if t:
                if isinstance(bills,list):
                    for i in bills:
                        if i.detail:
                            if i.detail.type !=int(t):
                                bills.remove(i)
                        else:
                            bills.remove(i)
                else:
                    bills = bills.filter(detail__type=int(t)).all()

            ctx['p'] = int(p) if p else ''
            ctx['t'] = int(t) if t else ''
            ctx['w'] = int(w) if w else ''
            ctx['s'] = s
            ctx['e'] = e

        elif action == 'export':
            if bills:
                e = xlwt.Workbook(encoding='utf-8')
                w = e.add_sheet(u'付费记录')
                w.write(0,0,'车牌号')
                w.write(0,1,'收费员')
                w.write(0,2,'入场时间')
                w.write(0,3,'离场时间')
                w.write(0,4,'停车时长')
                w.write(0,5,'车辆类型')
                w.write(0,6,'应收费用')
                w.write(0,7,'实收费用')
                w.write(0,8,'收费类型')
                w.write(0,9,'收费时间')
                row = 1
                for i  in bills:
                    w.write(row, 0, i.InAndOut.number if i.InAndOut else '')
                    w.write(row, 1, i.tollman)
                    w.write(row, 2, i.InAndOut.in_time if i.InAndOut else '')
                    w.write(row, 3, i.InAndOut.out_time if i.InAndOut else '')
                    w.write(row,4,i.parking_time)
                    w.write(row,5,i.InAndOut.vehicle_type_in if i.InAndOut else '')
                    w.write(row,6,i.payable)
                    w.write(row,7,i.payment)
                    w.write(row,8,i.detail.get_type_display if i.detail else '')
                    w.write(row,9,i.detail.time if i.detail else '')
                    row +=1
                output = io.BytesIO()
                e.save(output)
                # 重新定位到开始
                output.seek(0)
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename=bill.xls'
                response.write(output.getvalue())
                return response
    # print(11111)
    # te = InAndOut.objects.first()
    # print(te.in_time)
    # print(te.out_time)
    # print(get_price(te))

    ctx['parkinglots'] = ParkingLot.objects.all()
    ctx['workers'] = Worker.objects.all()
    ctx['objects'] = ctx['bills'] = bills
    return (ctx,'bill.html')


