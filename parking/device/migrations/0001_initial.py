# Generated by Django 2.0.4 on 2019-11-27 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parkinglot', '0002_auto_20191127_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=200, null=True, verbose_name='编号')),
                ('type', models.CharField(blank=True, max_length=200, null=True, verbose_name='类型')),
                ('name', models.CharField(max_length=200, verbose_name='名称')),
                ('brand', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('buy_time', models.DateTimeField(null=True, verbose_name='采购时间')),
                ('gate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Gate', verbose_name='所属出入口')),
                ('parkinglot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.ParkingLot', verbose_name='所属车场')),
            ],
            options={
                'verbose_name': '闸机',
                'verbose_name_plural': '闸机',
            },
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=200, null=True, verbose_name='编号')),
                ('type', models.CharField(blank=True, max_length=200, null=True, verbose_name='类型')),
                ('name', models.CharField(max_length=200, verbose_name='名称')),
                ('brand', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('buy_time', models.DateTimeField(null=True, verbose_name='采购时间')),
                ('gate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Gate', verbose_name='所属出入口')),
                ('parkinglot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.ParkingLot', verbose_name='所属车场')),
            ],
            options={
                'verbose_name': '摄像头',
                'verbose_name_plural': '摄像头',
            },
        ),
        migrations.CreateModel(
            name='GroundSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=200, null=True, verbose_name='编号')),
                ('type', models.CharField(blank=True, max_length=200, null=True, verbose_name='类型')),
                ('name', models.CharField(max_length=200, verbose_name='名称')),
                ('brand', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True, verbose_name='厂商')),
                ('buy_time', models.DateTimeField(null=True, verbose_name='采购时间')),
                ('gate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Gate', verbose_name='所属出入口')),
                ('parkinglot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.ParkingLot', verbose_name='所属车场')),
            ],
            options={
                'verbose_name': '地感',
                'verbose_name_plural': '地感',
            },
        ),
    ]
