# Generated by Django 2.2.3 on 2019-12-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0023_auto_20191219_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceptrecord',
            name='cam_ip',
            field=models.CharField(max_length=100, null=True, verbose_name='IP地址'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='closeup_pic',
            field=models.ImageField(null=True, upload_to='plate/%Y/%m/%d', verbose_name='车牌图片'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='color',
            field=models.CharField(max_length=100, null=True, verbose_name='车辆颜色'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='confidence',
            field=models.FloatField(null=True, verbose_name='置信度'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='direction',
            field=models.IntegerField(choices=[(0, '入'), (1, '出')], default=0, verbose_name='方向'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='logo',
            field=models.CharField(max_length=200, null=True, verbose_name='logo'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='park_id',
            field=models.CharField(max_length=100, null=True, verbose_name='park_id'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='plate_color',
            field=models.CharField(max_length=100, null=True, verbose_name='车牌颜色'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='plate_val',
            field=models.BooleanField(default=True, verbose_name='是否虚假车牌'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='time',
            field=models.DateTimeField(null=True, verbose_name='识别时间'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='triger_type',
            field=models.CharField(max_length=100, null=True, verbose_name='触发类型'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='vdc_type',
            field=models.CharField(max_length=100, null=True, verbose_name='出入口类型'),
        ),
        migrations.AddField(
            model_name='exceptrecord',
            name='vehicle_type',
            field=models.CharField(max_length=100, null=True, verbose_name='车辆类型'),
        ),
        migrations.AlterField(
            model_name='exceptrecord',
            name='picture',
            field=models.ImageField(null=True, upload_to='car/%Y/%m/%d', verbose_name='车辆图片'),
        ),
    ]
