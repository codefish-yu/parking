# Generated by Django 2.2.3 on 2019-11-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20191128_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=30, null=True, verbose_name='商家地址'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=30, null=True, verbose_name='商家名称'),
        ),
    ]