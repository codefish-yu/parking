from django.db import models


from meta.models import User, Product
from device.models import Camera
from parkinglot.models import ParkingLot, Worker, Gate


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
    out_time = models.DateTimeField(null=True, verbose_name='出场时间(用户端点击出场)')
    final_out_time = models.DateTimeField(null=True, verbose_name='实际出场时间')

    picture_in = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic_in = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')

    picture_out = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic_out = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')

    park_id = models.CharField(max_length=100, verbose_name='park_id')
    parkinglot = models.ForeignKey(ParkingLot, null=True, on_delete=models.SET_NULL, verbose_name='车场')
    
    cam_id_in = models.CharField(max_length=100, null=True, verbose_name='camera_id(Mac地址)')
    camera_in = models.ForeignKey(Camera, related_name='camera_in', null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    gate_in = models.ForeignKey(Gate, related_name='gate_in', null=True, on_delete=models.SET_NULL, verbose_name='入口')
    
    cam_id_out = models.CharField(max_length=100, null=True, verbose_name='camera_id(Mac地址)')
    camera_out = models.ForeignKey(Camera, related_name='camera_out', null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    gate_out = models.ForeignKey(Gate, related_name='gate_out', null=True, on_delete=models.SET_NULL, verbose_name='出口')
    
    vdc_type = models.CharField(max_length=100, null=True, verbose_name='出入口类型')
    enter_type = models.IntegerField(default=0, choices=[(0, '车牌识别'),(1, '扫码抬杆')], verbose_name='入场类型')
    leave_type = models.IntegerField(default=0, choices=[(0, '车牌识别'),(1, '扫码抬杆')], verbose_name='出场类型')
   
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
    status = models.IntegerField(default=0, choices=[(-1, '待入场'),(0,'入场'),(1,'已出场')], verbose_name='车辆状态')

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='停车用户')
    bill = models.OneToOneField('Bill', null=True, on_delete=models.SET_NULL, verbose_name='账单',related_name='InAndOut',blank=True)
    is_spec = models.IntegerField(default=0,choices=[(0,'正常'),(1,'特殊')])
    remark = models.CharField(max_length=30,null=True, verbose_name='备注信息')
    exception = models.IntegerField(default=0,choices=[(0,'正常'),(1,'异常')])
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

    def get_price(self):
        return 2
    def get_duration(self):
        return 2


class OpeningOrder(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '开闸指令'

    parkinglot = models.ForeignKey(ParkingLot, null=True, on_delete=models.CASCADE)
    gate = models.ForeignKey(Gate, null=True, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=[(0, '关闭'),(1, '打开'),(2, '需要打开')])

    in_and_out = models.ForeignKey('InAndOut', null=True, on_delete=models.CASCADE)


class Bill(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '账单'

    payable = models.FloatField(verbose_name='应付金额')
    payment = models.FloatField(verbose_name='实付金额')
    pay_time = models.DateTimeField(null=True, verbose_name='支付时间')
    pay_type = models.IntegerField(null=True, choices=[(0, '现金'),(1, '微信'),(2, '支付宝'),(3, '刷卡')], verbose_name='支付方式')
    tollman = models.ForeignKey(Worker,on_delete=models.SET_NULL,verbose_name='收费员',null=True,blank=True)
    parking_time = models.FloatField(null=True, verbose_name='停车时长(分钟)')
    status = models.IntegerField(default=0, choices=[(0, '未支付'),(1, '已支付'),(2,'已出场')])
    detail = models.ForeignKey('PayDetail',on_delete=models.SET_NULL,verbose_name='收费明细',related_name='detail',null=True,blank=True)

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)


class PayDetail(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '收费明细'

    time = models.DateTimeField(verbose_name='收费时间')
    type = models.IntegerField(default=0,choices=[(0,'全部'),(1,'手动免费开闸'),(2,'异常出车'),(3,'现金支付')],verbose_name='收费类型')
    price = models.FloatField(default=0,verbose_name='应收费用',null=True)
    real_price = models.FloatField(default=0,verbose_name='实收费用')

 
class ExceptRecord(models.Model):
    class Meta:
        verbose_name=verbose_name_plural='异常记录'


    picture = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')
    cam_id = models.CharField(max_length=100, null=True, verbose_name='camera_id(Mac地址)')
    camera = models.ForeignKey(Camera, related_name='except_camera', null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    gate = models.ForeignKey(Gate, related_name='except_gate', null=True, on_delete=models.SET_NULL, verbose_name='口')
    direction = models.IntegerField(default=0,verbose_name='方向',choices=[(0,'出'),(1,'入')])
    plate_color = models.CharField(max_length=100, null=True,verbose_name='车牌颜色')
    logo = models.CharField(max_length=200, null=True,verbose_name='logo')
    park_id = models.CharField(max_length=100, null=True,verbose_name='park_id')
    cam_ip = models.CharField(max_length=100, null=True, verbose_name='IP地址')
    plate_val = models.BooleanField(default=True, verbose_name='是否虚假车牌')
    confidence = models.FloatField(null=True, verbose_name='置信度')
    color = models.CharField(max_length=100, null=True,verbose_name='车辆颜色')
    vdc_type = models.CharField(max_length=100, null=True, verbose_name='出入口类型')
    triger_type = models.CharField(max_length=100, null=True, verbose_name='触发类型')
    vehicle_type = models.CharField(max_length=100, null=True,verbose_name='车辆类型')
    update_time = models.DateTimeField(null=True, verbose_name='识别时间')
    status = models.IntegerField(default=0,verbose_name='状态',choices=[(0,'待处理'),(1,'已处理')])


