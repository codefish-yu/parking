from django.db import models
from realtime.models import InAndOut 
from parkinglot.models import *
from meta.models import *
from meta.models import User
from parkinglot.models import Worker


# Create your models here.


# class account_record(models.Model):
# 	class Meta:
# 		verbose_name=verbose_name_plural='收银记录'

class WorkRecord(models.Model):
	class Meta:
		verbose_name = verbose_name_plural ='值班记录'

	time = models.DateTimeField(null=True,verbose_name='上岗时间')
	duration = models.FloatField(default=0,verbose_name='值班时长')
	spec_num = models.IntegerField(default=0,verbose_name='特放车辆')
	worker = models.ForeignKey(User,on_delete=models.SET_NULL,verbose_name='员工',null=True)
	offline = models.DateTimeField(null=True,verbose_name='断线时间')
	parkinglot = models.ForeignKey(ParkingLot,null=True,on_delete=models.SET_NULL,verbose_name='上岗车场')
	gate = models.ForeignKey(Gate,verbose_name='值班口',null=True,on_delete=models.SET_NULL)

class SpecRecord(models.Model):
	class Meta:
		verbose_name=verbose_name_plural='特放记录'

	tollman = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,verbose_name='操作员')
	record = models.ForeignKey(InAndOut,null=True,on_delete=models.SET_NULL,verbose_name='记录')

			
	
		




