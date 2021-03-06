# Generated by Django 2.2.3 on 2019-12-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0034_ticketrecord_coucode'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrecord',
            name='price',
            field=models.FloatField(default=0, null=True, verbose_name='单价'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='amount',
            field=models.IntegerField(null=True, verbose_name='购买上限'),
        ),
        migrations.AlterField(
            model_name='ticketrecord',
            name='buy_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='购买时间'),
        ),
    ]
