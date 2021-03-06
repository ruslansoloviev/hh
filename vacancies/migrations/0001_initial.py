# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-11-22 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metro',
            fields=[
                ('station_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=30)),
                ('line_id', models.IntegerField(null=True)),
                ('line_name', models.CharField(max_length=30)),
                ('lat', models.DecimalField(decimal_places=3, max_digits=8, null=True)),
                ('lng', models.DecimalField(decimal_places=3, max_digits=8, null=True)),
            ],
        ),
    ]
