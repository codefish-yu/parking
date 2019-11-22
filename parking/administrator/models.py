from django.db import models

# Create your models here.


'''系统设置模块'''


class AdminUser(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '系统用户'

    pass


class Role(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户角色'

    pass


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
