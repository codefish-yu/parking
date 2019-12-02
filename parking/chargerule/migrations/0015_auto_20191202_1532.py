# Generated by Django 2.2.3 on 2019-12-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargerule', '0014_remove_cardtype_suit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtype',
            name='relax_end',
            field=models.CharField(max_length=30, null=True, verbose_name='休息结束'),
        ),
        migrations.AlterField(
            model_name='cardtype',
            name='relax_start',
            field=models.CharField(max_length=30, null=True, verbose_name='休息开始'),
        ),
        migrations.AlterField(
            model_name='cardtype',
            name='work_end',
            field=models.CharField(max_length=30, null=True, verbose_name='工作结束'),
        ),
        migrations.AlterField(
            model_name='cardtype',
            name='work_start',
            field=models.CharField(max_length=30, null=True, verbose_name='工作开始'),
        ),
    ]
