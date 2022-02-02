# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-21 03:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplyorder',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Customer'),
        ),
        migrations.AlterField(
            model_name='supplyorder',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('PAID', 'PAID'), ('CONFIRMED', 'CONFIRMED'), ('CANCELLED', 'CANCELLED'), ('SHIPPED', 'SHIPPED'), ('DELIVERED', 'DELIVERED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=255),
        ),
    ]