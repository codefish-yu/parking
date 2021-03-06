# Generated by Django 2.0.4 on 2019-11-27 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True, verbose_name='用户账号')),
                ('user_pass', models.CharField(max_length=30, unique=True, verbose_name='密码')),
                ('phone', models.IntegerField(default=0, unique=True, verbose_name='电话号码')),
                ('sex', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, null=True, verbose_name='性别')),
                ('real_name', models.CharField(max_length=30, unique=True, verbose_name='姓名')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
            ],
            options={
                'verbose_name': '系统用户',
                'verbose_name_plural': '系统用户',
            },
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='ip')),
                ('operation', models.CharField(blank=True, max_length=100, null=True, verbose_name='操作')),
                ('content', models.CharField(blank=True, max_length=100, null=True, verbose_name='操作内容')),
                ('model', models.CharField(blank=True, max_length=100, null=True, verbose_name='操作模块')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('create_day', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.AdminUser', verbose_name='操作用户')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(default='', max_length=100, unique=True, verbose_name='菜单名称')),
                ('url', models.CharField(max_length=200, null=True, unique=True, verbose_name='相对路径url')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_name', models.CharField(default='', max_length=100, verbose_name='操作名称')),
                ('action', models.CharField(default='', max_length=100, verbose_name='方法名')),
            ],
            options={
                'verbose_name': '操作(功能)',
                'verbose_name_plural': '操作(功能)',
            },
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '系统类别明细',
                'verbose_name_plural': '系统类别明细',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100, unique=True, verbose_name='用户名')),
                ('detail', models.CharField(max_length=200, null=True, verbose_name='说明')),
            ],
            options={
                'verbose_name': '用户角色',
                'verbose_name_plural': '用户角色',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '系统参数',
                'verbose_name_plural': '系统参数',
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='operation',
            field=models.ManyToManyField(to='administrator.Operation', verbose_name='操作'),
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.Menu'),
        ),
        migrations.AddField(
            model_name='authority',
            name='child_menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_menu', to='administrator.Menu', verbose_name='二级菜单'),
        ),
        migrations.AddField(
            model_name='authority',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_menu', to='administrator.Menu', verbose_name='以及菜单'),
        ),
        migrations.AddField(
            model_name='authority',
            name='operation',
            field=models.ManyToManyField(to='administrator.Operation'),
        ),
        migrations.AddField(
            model_name='authority',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='role_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.Role'),
        ),
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['create_day'], name='create_day_idx'),
        ),
    ]
