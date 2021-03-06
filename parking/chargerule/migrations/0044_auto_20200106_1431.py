# Generated by Django 2.0.4 on 2020-01-06 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0043_auto_20200103_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoupon',
            name='ticket_record',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='chargerule.TicketRecord'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercoupon',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chargerule.Coupons'),
        ),
        migrations.AlterField(
            model_name='usercoupon',
            name='status',
            field=models.IntegerField(choices=[(0, '未使用'), (1, '已使用')], default=0),
        ),
    ]
