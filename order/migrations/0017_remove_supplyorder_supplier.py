# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-22 23:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20220123_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplyorder',
            name='supplier',
        ),
    ]
