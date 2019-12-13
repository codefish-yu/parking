# Generated by Django 2.2.3 on 2019-12-11 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0008_merge_20190812_0048'),
        ('realtime', '0015_merge_20191211_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='product',
        ),
        migrations.AddField(
            model_name='paydetail',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meta.Product'),
        ),
    ]