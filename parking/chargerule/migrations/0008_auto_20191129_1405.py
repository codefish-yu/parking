# Generated by Django 2.2.3 on 2019-11-29 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0007_merge_20191129_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='my_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chargerule.CardType', verbose_name='卡片类型'),
        ),
    ]
