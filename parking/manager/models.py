from django.db import models
from parkinglot.models import Worker

# class Worker(models.Model):
#     class Meta:
#         verbose_name = verbose_name_plural = '车场员工'

#     number = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='员工号')
#     name = models.CharField(max_length=100, null=True, blank=True, verbose_name='员工名称')
#     birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
#     sex = models.IntegerField(choices=[(0, '男'),(1, '女')], verbose_name='性别')

#     is_delete = models.IntegerField(choices=[(0, '否'),(1, '是')], default=0, verbose_name='是否删除')
#     forbidden = models.IntegerField(choices=[(0, '启用'),(1, '禁用')], default=0,  verbose_name='是否禁用')
#     parkinglot = models.ForeignKey(ParkingLot, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属车场')
#     user = models.ForeignKey(User,verbose_name='员工微信',null=True,on_delete=models.SET_NULL,blank=True)

#     create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     update_time = models.DateTimeField(auto_now=True, blank=True, null=True)

# Create your models here.


