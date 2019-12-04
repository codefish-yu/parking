from django.db import models


from device.models import Camera
from parkinglot.models import ParkingLot


class InAndOut(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '出入场记录'

    number = models.CharField(max_length=100, verbose_name='车牌')
    color = models.CharField(max_length=100, verbose_name='车辆颜色')
    logo = models.CharField(max_length=200, verbose_name='logo')
    start_time = models.DateTimeField(null=True, verbose_name='识别时间')
    picture = models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片')
    closeup_pic = models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片')

    park_id = models.CharField(max_length=200, verbose_name='park_id')
    parkinglot = models.ForeignKey(ParkingLot, null=True, on_delete=models.SET_NULL, verbose_name='车场')
    
    cam_id = models.CharField(max_length=200, null=True, verbose_name='camera_id(Mac地址)')
    camera = models.ForeignKey(Camera, null=True, on_delete=models.SET_NULL, verbose_name='摄像头')
    
    
    # valid = models.BooleanField(default=True, verbose_name='是否虚假车牌')
    # confidence = models.FloatField(null=True, verbose_name='置信度')
    # car_type = models.CharField(max_length=200, verbose_name='车辆类型')
    # vdc_type = models.CharField(max_length=200, null=True, verbose_name='出入口类型')
    # triger_type = models.IntegerField(null=True, choices=[('video', '视频触发'),('hwtriger', '地感触发'),('swtriger', '软触发')], verbose_name='触发类型')
    
    def car_pic(self):
        return self.picture.url if self.picture else ''

    def plate_pic(self):
        return self.closeup_pic.url if self.closeup_pic else ''