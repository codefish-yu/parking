# Generated by Django 2.2.3 on 2019-11-26 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0002_auto_20191126_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('use_type', models.IntegerField(choices=[(0, '停车场内'), (1, '停车场入口'), (2, '停车场出口')], unique=True, verbose_name='使用类型')),
                ('ctrl_type', models.IntegerField(choices=[(0, '临停车控制'), (1, '入口不控制'), (2, '控制入车类型'), (3, '不控制只抓拍'), (4, '时间控制'), (5, '月租车控制'), (6, '卡票控制')], unique=True, verbose_name='控制类型')),
                ('zone', models.IntegerField(choices=[(0, '地面'), (1, '地库')], unique=True, verbose_name='所属区域')),
                ('monitor', models.CharField(blank=True, max_length=30, verbose_name='所属监控')),
                ('charge_rule', models.IntegerField(choices=[(0, '按出口所在区域收费'), (1, '按入口所在区域收费')], verbose_name='收费规则')),
                ('parkinglot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkinglot.ParkingLot', verbose_name='所属车场')),
            ],
        ),
    ]
