from django.db import models

# Create your models here.


'''系统设置模块'''


class AdminUser(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '系统用户'

    status = models.IntegerField(unique=True,default=0)
    user_name = models.CharField(max_length=30, unique=True, verbose_name='用户账号')
    user_pass = models.CharField(max_length=30, unique=True, verbose_name='密码')
    role_name = models.ForeignKey('Role',null=True,on_delete=models.CASCADE)
    phone = models.IntegerField(unique=True,verbose_name='电话号码',default=0)
    sex = models.IntegerField(null=True,choices=[(0,'男'),(1,'女')],verbose_name='性别' ,default=0)
    real_name = models.CharField(max_length=30, unique=True, verbose_name='姓名')
    remark = models.CharField(max_length=100,verbose_name='备注')

    def display_sex(self):
        if self.sex == 0:
            return '男'
        else:
            return '女'


class Role(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户角色'

    role_name = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    detail = models.CharField(max_length=200, null=True, verbose_name='说明')


class Menu(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '菜单'

    pass


class Operation(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '操作(功能)'

    pass


class Settings(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '系统参数'

    pass


class Options(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '系统类别明细'

    pass


class Log(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '操作日志'
        indexes = [
            models.Index(
                fields=['create_day'],
                name='create_day_idx',
            ),
        ]
    ip = models.CharField(max_length=100, null=True, blank=True, verbose_name='ip')
    operation = models.CharField(max_length=100, null=True, blank=True, verbose_name='操作')
    content = models.CharField(max_length=100, null=True, blank=True, verbose_name='操作内容')
    model = models.CharField(max_length=100, null=True, blank=True, verbose_name='操作模块')
    user = models.ForeignKey(on_delete=models.SET_NULL, null=True, blank=True, verbose_name='操作用户')

    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_day = models.IntegerField(null=True, blank=True)

 
class ParkingLot(models.Model):
    class meta:
        verbose_name = verbose_name_plural = '停车场'

    status = models.IntegerField(unique=True,default=0)
    name = models.CharField(max_length=30, unique=True, verbose_name='停车场名称')
    zone_num = models.IntegerField(unique=True,default=0,verbose_name='区域数')
    place_num = models.IntegerField(unique=True,default=0,verbose_name='车位数')

   
