# Generated by Django 2.2.3 on 2020-01-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0042_ticketrecord_qrcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketrecord',
            name='qrcode',
        ),
        migrations.AddField(
            model_name='ticketrecord',
            name='qrrandom',
            field=models.CharField(max_length=30, null=True, verbose_name='随机数'),
        ),
    ]
