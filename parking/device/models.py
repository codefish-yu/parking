from django.db import models

# Create your models here.

from parkinglot.models import ParkingLot, Gate

'''设备管理模块'''


class Camera(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '摄像头'

    number = models.CharField(max_length=200, null=True, blank=True, verbose_name='编号')
    type = models.CharField(max_length=200, null=True, blank=True, verbose_name='类型')
    name = models.CharField(max_length=200, verbose_name='名称')
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    manufacturer = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    buy_time = models.DateTimeField(null=True, verbose_name='采购时间')

    parkinglot = models.ForeignKey(ParkingLot, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属车场')
    gate = models.ForeignKey(Gate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属出入口')

    def __str__(self):
        return self.name


class Brake(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '闸机'

    number = models.CharField(max_length=200, null=True, blank=True, verbose_name='编号')
    type = models.CharField(max_length=200, null=True, blank=True, verbose_name='类型')
    name = models.CharField(max_length=200, verbose_name='名称')
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    manufacturer = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    buy_time = models.DateTimeField(null=True, verbose_name='采购时间')

    parkinglot = models.ForeignKey(ParkingLot, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属车场')
    gate = models.ForeignKey(Gate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属出入口')
 
    def __str__(self):
        return self.name


class GroundSensor(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '地感'

    number = models.CharField(max_length=200, null=True, blank=True, verbose_name='编号')
    type = models.CharField(max_length=200, null=True, blank=True, verbose_name='类型')
    name = models.CharField(max_length=200, verbose_name='名称')
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    manufacturer = models.CharField(max_length=200, null=True, blank=True, verbose_name='厂商')
    buy_time = models.DateTimeField(null=True, verbose_name='采购时间')

    parkinglot = models.ForeignKey(ParkingLot, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属车场')
    gate = models.ForeignKey(Gate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属出入口')
 
    def __str__(self):
        return self.name



        