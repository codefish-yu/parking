# Generated by Django 2.2.3 on 2019-12-20 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0007_worker_user'),
        ('account', '0006_workrecord_offline'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrecord',
            name='gate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Gate', verbose_name='值班口'),
        ),
        migrations.AddField(
            model_name='workrecord',
            name='parkinglot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.ParkingLot', verbose_name='上岗车场'),
        ),
    ]