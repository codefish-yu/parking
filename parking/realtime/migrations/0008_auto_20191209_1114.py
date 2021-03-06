# Generated by Django 2.2.3 on 2019-12-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0007_pay_paydetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='price',
            field=models.FloatField(default=0, null=True, verbose_name='应收费用'),
        ),
        migrations.AddField(
            model_name='pay',
            name='real_price',
            field=models.FloatField(default=0, verbose_name='实收费用'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='car_type',
            field=models.IntegerField(choices=[(0, '临停车'), (1, '月租车')], default=0, null=True, verbose_name='车辆类型'),
        ),
    ]
