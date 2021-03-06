# Generated by Django 2.0.4 on 2019-12-18 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0004_gate_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(verbose_name='自定义日期')),
                ('ifwork', models.BooleanField(verbose_name='是否工作日')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('parkinglot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkinglot.ParkingLot')),
            ],
            options={
                'verbose_name': '自定义工作日、非工作日(默认是按周内周末划分)',
                'verbose_name_plural': '自定义工作日、非工作日(默认是按周内周末划分)',
            },
        ),
    ]
