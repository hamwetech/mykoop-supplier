# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-21 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0006_auto_20201111_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]