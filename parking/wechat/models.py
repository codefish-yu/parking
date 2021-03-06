from django.db import models

# Create your models here.
 

from meta.models import User
from parkinglot.models import ParkingLot, Gate


class MyPlate(models.Model):
	class Meta:
		verbose_name = '我的车牌'

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	plate = models.CharField(max_length=100, verbose_name='车牌')


class Problem(models.Model):
	class Meta:
		verbose_name = '用户提交异常'

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	plate = models.CharField(max_length=100, verbose_name='车牌')
	parkinglot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
	gate = models.ForeignKey(Gate, null=True, on_delete=models.SET_NULL)
	status = models.IntegerField(default=0,choices=[(0,'待处理'),(1,'已处理')])

	update_time = models.DateTimeField(auto_now_add=True)
