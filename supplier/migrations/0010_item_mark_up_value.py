# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-22 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0009_auto_20220122_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mark_up_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
