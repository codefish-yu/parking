from django.db import models

# Create your models here.
 

from meta.models import User


class MyPlate(models):
	class Meta:
		verbose_name = '我的车牌'

	user = models.Foreignkey(User, on_delete=models.CASCADE)
	plate = models.CharField(max_length=100, verbose_name='车牌')
