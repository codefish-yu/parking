# Generated by Django 2.2.3 on 2019-12-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0025_auto_20191205_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtype',
            name='name',
            field=models.CharField(max_length=30, verbose_name='名称'),
        ),
    ]
