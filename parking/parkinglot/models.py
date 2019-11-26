from django.db import models

# Create your models here.


'''停车场管理模块'''
class ParkingLot(models.Model):
    class meta:
        verbose_name = verbose_name_plural = '停车场管理'

    status = models.IntegerField(default=0)
    name = models.CharField(max_length=30, unique=True, verbose_name='停车场名称')
    zone_num = models.IntegerField(default=0,verbose_name='区域数')
    place_num = models.IntegerField(default=0,verbose_name='车位数')



class Gate(models.Model):
	class meta:
		verbose_name = verbose_name_plural = '进出口管理'

	usertype = [(0,'停车场内'),(1,'停车场入口'),(2,'停车场出口')]
	ctrltype = [(0,'临停车控制'),(1,'入口不控制'),(2,'控制入车类型'),(3,'不控制只抓拍'),(4,'时间控制'),(5,'月租车控制'),(6,'卡票控制')]
	zones = [(0,'地面'),(1,'地库')]
	rules = [(0,'按出口所在区域收费'),(1,'按入口所在区域收费')]

	status = models.IntegerField(default=0)
	use_type = models.IntegerField(verbose_name='使用类型',choices=usertype,default=0)
	ctrl_type = models.IntegerField(verbose_name='控制类型',choices=ctrltype,default=0)
	parkinglot = models.ForeignKey('ParkingLot',null=True,on_delete=models.CASCADE,verbose_name='所属车场')
	zone = models.IntegerField(verbose_name='所属区域',choices=zones,default=0)
	monitor = models.CharField(max_length=30,blank=True,verbose_name='所属监控')
	charge_rule = models.IntegerField(choices=rules,verbose_name='收费规则',default=0)

    


	
		
