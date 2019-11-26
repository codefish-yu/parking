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

    role_name = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    detail = models.CharField(max_length=200, null=True, verbose_name='说明')

    def get_auth(self):
        auths = Authority.objects.filter(role=self)
        menu = set()
        child_menu = set()
        operation = set()

        for i in auths:
            menu.add(i.menu.id)
            child_menu.add(i.child_menu.id)
            for j in i.operation.all():
                operation.add(j.id)

        return {'menu': menu, 'child_menu': child_menu, 'operation': operation}


class Menu(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '菜单'

    menu_name = models.CharField(max_length=100, default='', unique=True, verbose_name='菜单名称')
    parent = models.ForeignKey('Menu', null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, unique=True, null=True, verbose_name='相对路径url')

    operation = models.ManyToManyField('Operation', verbose_name='操作')


class Operation(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '操作(功能)'

    operation_name = models.CharField(max_length=100, default='', verbose_name='操作名称')
    action = models.CharField(max_length=100, default='', verbose_name='方法名')


class Authority(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '权限'

    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL,null=True, related_name='parent_menu', verbose_name='以及菜单')
    child_menu = models.ForeignKey(Menu, on_delete=models.SET_NULL,null=True, related_name='child_menu', verbose_name='二级菜单')
    operation = models.ManyToManyField(Operation)


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
