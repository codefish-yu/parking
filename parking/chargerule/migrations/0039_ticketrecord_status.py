# Generated by Django 2.2.3 on 2019-12-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0038_ticketrecord_superpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrecord',
            name='status',
            field=models.IntegerField(choices=[(0, '审核中'), (1, '审核通过'), (2, '审核失败')], default=0),
        ),
    ]
