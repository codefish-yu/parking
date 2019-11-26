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



class Worker(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '车场员工'

    number = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='员工号')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='员工名称')
    birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    sex = models.IntegerField(choices=[(0, '男'),(1, '女')], verbose_name='性别')

    is_delete = models.IntegerField(choices=[(0, '否'),(1, '是')], verbose_name='是否删除')
    forbidden = models.IntegerField(choices=[(0, '否'),(1, '是')], verbose_name='是否禁用')
    parkinglot = models.ForeignKey(ParkingLot, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属车场')

    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True)
