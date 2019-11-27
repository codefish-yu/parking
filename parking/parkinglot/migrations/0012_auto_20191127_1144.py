# Generated by Django 2.2.3 on 2019-11-27 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0011_merge_20191127_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='forbidden',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='是否禁用'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='is_delete',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='是否删除'),
        ),
    ]