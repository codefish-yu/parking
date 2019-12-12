# Generated by Django 2.0.4 on 2019-12-12 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0008_merge_20190812_0048'),
        ('realtime', '0016_auto_20191211_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paydetail',
            name='product',
        ),
        migrations.AddField(
            model_name='bill',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meta.Product'),
        ),
    ]
