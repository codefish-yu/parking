# Generated by Django 2.2.3 on 2019-11-29 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
        ('chargerule', '0004_auto_20191129_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.AdminUser', verbose_name='持卡人'),
        ),
        migrations.AlterField(
            model_name='card',
            name='my_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chargerule.Card', verbose_name='卡片类型'),
        ),
    ]
