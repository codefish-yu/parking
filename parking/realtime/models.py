from django.db import models


from device.models import Camera
from parkinglot.models import ParkingLot


class InAndOut(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '出入场记录'

    number = models.CharField(max_length=100, verbose_name='车牌')
    color_in = models.CharField(max_length=100, verbose_name='车辆颜色')
    plate_color_in = models.CharField(max_length=100, verbose_name='车牌颜色')
    logo_in = models.CharField(max_length=200, verbose_name='logo')

    color_out = models.CharField(max_length=100, verbose_name='车辆颜色')
    plate_color_out = models.CharField(max_length=100, verbose_name='车牌颜色')
    logo_out = models.CharField(max_length=200, verbose_name='logo')

    in_time = models.DateTimeField(null=True, verbose_name='入口识别时间')
    out_time = models.DateTimeField(null=True, verbose_name='出口识别时间')
    picture_in = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic_in = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')

    picture_out = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic_out = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')

    park_id = models.CharField(max_length=100, verbose_name='park_id')
    parkinglot = models.ForeignKey(ParkingLot, null=True, on_delete=models.SET_NULL, verbose_name='车场')
    
    cam_id_in = models.CharField(max_length=100, null=True, verbose_name='camera_id(Mac地址)')
    camera_in = models.ForeignKey(Camera, related_name='camera_in', null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    
    cam_id_out = models.CharField(max_length=100, null=True, verbose_name='camera_id(Mac地址)')
    camera_out = models.ForeignKey(Camera, related_name='camera_out', null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    
    vdc_type = models.CharField(max_length=100, null=True, verbose_name='出入口类型')
   
    cam_ip_in = models.CharField(max_length=100, null=True, verbose_name='IP地址')
    plate_val_in = models.BooleanField(default=True, verbose_name='是否虚假车牌')
    confidence_in = models.FloatField(null=True, verbose_name='置信度')
    vehicle_type_in = models.CharField(max_length=100, verbose_name='车辆类型')
    triger_type_in = models.CharField(max_length=100, null=True, verbose_name='触发类型')

    cam_ip_out = models.CharField(max_length=100, null=True, verbose_name='IP地址')
    plate_val_out = models.BooleanField(default=True, verbose_name='是否虚假车牌')
    confidence_out = models.FloatField(null=True, verbose_name='置信度')
    vehicle_type_out = models.CharField(max_length=100, verbose_name='车辆类型')
    triger_type_out = models.CharField(max_length=100, null=True, verbose_name='触发类型')

    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')

    bill = models.ForeignKey('Bill', null=True, on_delete=models.SET_NULL, verbose_name='账单')
    # params = {
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
    def car_pic_in(self):
        return self.picture_in.url if self.picture_in else ''

    def plate_pic_in(self):
        return self.closeup_pic_in.url if self.closeup_pic_in else ''

    def car_pic_out(self):
        return self.picture_out.url if self.picture_out else ''

    def plate_pic_out(self):
        return self.closeup_pic_out.url if self.closeup_pic_out else ''


class Bill(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '账单'

    payable = models.FloatField(verbose_name='应付金额')
    payment = models.FloatField(verbose_name='实付金额')
    pay_time = models.DateTimeField(null=True, verbose_name='支付时间')
    pay_type = models.IntegerField(null=True, choices=[(0, '现金'),(1, '微信'),(2, '支付宝'),(3, '刷卡')], verbose_name='支付方式')

    parking_time = models.FloatField(null=True, verbose_name='停车时长(分钟)')
    # card = 
    # coupun = 
    # 滞留时间, 滞留收费
    status = models.IntegerField(default=0, choices=[(0, '未支付'),(1, '已支付')])


