# Generated by Django 2.2.3 on 2019-12-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0020_cardtype_is_diff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtype',
            name='is_diff',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0),
        ),
    ]