# Generated by Django 2.0.4 on 2019-11-25 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_auto_20191125_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_menu', to='administrator.Menu', verbose_name='二级菜单')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_menu', to='administrator.Menu', verbose_name='以及菜单')),
                ('operation', models.ManyToManyField(to='administrator.Operation')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
            },
        ),
    ]