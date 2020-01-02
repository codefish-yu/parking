from django.db import models

# Create your models here.
 

from meta.models import User


class MyPlate(models.Model):
	class Meta:
		verbose_name = '我的车牌'

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	plate = models.CharField(max_length=100, verbose_name='车牌')
