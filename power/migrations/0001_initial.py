# Generated by Django 3.1.1 on 2020-10-15 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='区域名')),
                ('client', models.GenericIPAddressField(help_text='区域IP')),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='宿舍楼名')),
                ('szu_id', models.SmallIntegerField(db_index=True, help_text='在深大系统中的id')),
                ('campus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='power.campus', verbose_name='宿舍楼所在区域')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.SmallIntegerField(db_index=True, verbose_name='宿舍房号')),
                ('power_data', models.JSONField(null=True, verbose_name='电量记录')),
                ('campus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='power.campus', verbose_name='宿舍所在区域')),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='power.building')),
            ],
            options={
                'unique_together': {('building', 'room_no')},
            },
        ),
    ]
