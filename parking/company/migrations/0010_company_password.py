# Generated by Django 2.2.3 on 2019-12-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20191209_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='password',
            field=models.CharField(default='123456', max_length=30, verbose_name='密码'),
        ),
    ]
