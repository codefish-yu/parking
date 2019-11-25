from django.db import models

# Create your models here.


'''系统设置模块'''


class AdminUser(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '系统用户'

    user_name = models.CharField(max_length=30, unique=True, verbose_name='用户账号')
    password = models.CharField(max_length=30, unique=True, verbose_name='密码')
    role_name = models.ForeignKey('Role',null=True,on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=30,unique=True,verbose_name='电话号码')
    sex = models.IntegerField(null=True,choices=[(0,'男'),(1,'女')],verbose_name='性别')
    real_name = models.CharField(max_length=30, unique=True, verbose_name='姓名')
    belong_business = models.ForeignKey('Business',null=True,on_delete=models.CASCADE)
    remark = models.CharField(max_length=100,verbose_name='备注')


class Business(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '商家'

    business_name = models.CharField(max_length=30, unique=True, verbose_name='商家名称')


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

    pass
