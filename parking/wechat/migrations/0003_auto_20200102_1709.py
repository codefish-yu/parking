# Generated by Django 2.0.4 on 2020-01-02 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_problem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='gate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='parkinglot.Gate'),
        ),
    ]
