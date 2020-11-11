# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-11-10 18:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_customerorder_agro_dealer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplyorder',
            name='supplier',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier'),
        ),
    ]