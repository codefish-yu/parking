# Generated by Django 2.2.3 on 2019-11-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0010_auto_20191129_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='holidays',
            field=models.TextField(blank=True, null=True, verbose_name='节假日'),
        ),
    ]