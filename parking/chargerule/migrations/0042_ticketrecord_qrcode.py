# Generated by Django 2.2.3 on 2020-01-03 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0041_auto_20191231_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrecord',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcode/', verbose_name='动态码'),
        ),
    ]
