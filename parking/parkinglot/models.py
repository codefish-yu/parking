from django.db import models

# Create your models here.


'''停车场管理模块'''
class ParkingLot(models.Model):
    class meta:
        verbose_name = verbose_name_plural = '停车场'

    status = models.IntegerField(unique=True,default=0)
    name = models.CharField(max_length=30, unique=True, verbose_name='停车场名称')
    zone_num = models.IntegerField(unique=True,default=0,verbose_name='区域数')
    place_num = models.IntegerField(unique=True,default=0,verbose_name='车位数')
