# Generated by Django 2.2.3 on 2019-11-29 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0002_auto_20191127_1210'),
        ('company', '0007_auto_20191128_1909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': '商户', 'verbose_name_plural': '商户'},
        ),
        migrations.AddField(
            model_name='company',
            name='parkinglot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkinglot.ParkingLot'),
        ),
    ]
