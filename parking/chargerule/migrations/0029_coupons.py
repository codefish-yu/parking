# Generated by Django 2.0.4 on 2019-12-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0028_baserule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, '打折券'), (1, '代金券'), (2, '抵扣券'), (3, '满时券')])),
                ('name', models.CharField(max_length=200, verbose_name='名称')),
                ('detail', models.CharField(max_length=200, verbose_name='说明')),
                ('rate', models.FloatField(blank=True, null=True, verbose_name='折扣率')),
                ('money', models.FloatField(blank=True, null=True, verbose_name='金额')),
                ('hours', models.FloatField(blank=True, null=True, verbose_name='小时数')),
                ('money1', models.FloatField(blank=True, null=True, verbose_name='金额')),
                ('hours1', models.FloatField(blank=True, null=True, verbose_name='小时数')),
                ('money2', models.FloatField(blank=True, null=True, verbose_name='金额')),
                ('hours2', models.FloatField(blank=True, null=True, verbose_name='小时数')),
                ('money3', models.FloatField(blank=True, null=True, verbose_name='金额')),
                ('hours3', models.FloatField(blank=True, null=True, verbose_name='小时数')),
                ('money4', models.FloatField(blank=True, null=True, verbose_name='金额')),
                ('hours4', models.FloatField(blank=True, null=True, verbose_name='小时数')),
                ('is_delete', models.IntegerField(choices=[(0, '未删除'), (1, '已删除')], default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': '优惠券',
                'verbose_name_plural': '优惠券',
            },
        ),
    ]
