# Generated by Django 2.2.3 on 2019-12-19 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0008_merge_20190812_0048'),
        ('parkinglot', '0006_auto_20191218_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='meta.User', verbose_name='员工微信'),
        ),
    ]