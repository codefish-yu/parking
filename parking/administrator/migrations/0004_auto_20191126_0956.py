# Generated by Django 2.0.4 on 2019-11-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_authority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='action',
            field=models.CharField(default='', max_length=100, verbose_name='方法名'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='operation_name',
            field=models.CharField(default='', max_length=100, verbose_name='操作名称'),
        ),
    ]
