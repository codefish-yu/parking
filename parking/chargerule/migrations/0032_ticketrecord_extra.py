# Generated by Django 2.2.3 on 2019-12-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0031_auto_20191220_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrecord',
            name='extra',
            field=models.IntegerField(default=0, verbose_name='余量'),
        ),
    ]
