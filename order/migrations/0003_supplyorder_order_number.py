# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-30 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201030_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplyorder',
            name='order_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]