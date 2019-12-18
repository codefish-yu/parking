from django.db import models
from realtime.models import InAndOut 
from meta.models import *

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
			
	
		




