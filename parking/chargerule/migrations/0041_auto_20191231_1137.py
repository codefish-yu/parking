# Generated by Django 2.2.3 on 2019-12-31 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0040_auto_20191231_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketrecord',
            name='status',
            field=models.IntegerField(choices=[(0, '待审核'), (1, '已通过'), (2, '审核失败')], default=0),
        ),
    ]
