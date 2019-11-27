# Generated by Django 2.2.3 on 2019-11-27 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0009_auto_20191126_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkinglot',
            name='name',
            field=models.CharField(max_length=30, verbose_name='停车场名称'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='place_num',
            field=models.IntegerField(default=0, null=True, verbose_name='泊位数'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='zone_name',
            field=models.CharField(max_length=30, null=True, verbose_name='区域名称'),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('car_type', models.CharField(choices=[(0, '小型车'), (1, '中型车'), (2, '大型车')], max_length=30, null=True, verbose_name='车辆类型')),
                ('use_type', models.IntegerField(choices=[(0, '临停车'), (1, '长租车')], default=0, null=True, verbose_name='使用类型')),
                ('parkinglot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkinglot.ParkingLot', verbose_name='所属车场')),
                ('zone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkinglot.Zone', verbose_name='所属区域')),
            ],
            options={
                'verbose_name': '泊位管理',
                'verbose_name_plural': '泊位管理',
            },
        ),
    ]
