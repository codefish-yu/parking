# Generated by Django 2.2.3 on 2019-11-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0014_auto_20191127_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='car_type',
            field=models.IntegerField(choices=[(0, '小型车'), (1, '中型车'), (2, '大型车')], null=True, verbose_name='车辆类型'),
        ),
    ]