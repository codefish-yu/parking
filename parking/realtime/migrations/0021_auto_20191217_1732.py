# Generated by Django 2.2.3 on 2019-12-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0020_auto_20191213_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='inandout',
            name='id_spec',
            field=models.IntegerField(choices=[(0, '正常'), (1, '特殊')], default=0),
        ),
        migrations.AddField(
            model_name='inandout',
            name='remark',
            field=models.CharField(max_length=30, null=True, verbose_name='备注信息'),
        ),
    ]
