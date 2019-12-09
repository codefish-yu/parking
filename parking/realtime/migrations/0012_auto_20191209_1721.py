# Generated by Django 2.2.3 on 2019-12-09 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0011_auto_20191209_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='detail',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detail', to='realtime.PayDetail', verbose_name='收费明细'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='tollman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Worker', verbose_name='收费员'),
        ),
    ]
