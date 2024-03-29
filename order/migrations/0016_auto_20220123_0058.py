# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-22 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_customer_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplyorder',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supplyorder',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supplyorder',
            name='payment_mode',
            field=models.CharField(choices=[('CASH', 'CASH'), ('MOBILE MONEY', 'MOBILE MONEY'), ('HIRE PURCHASE', 'HIRE PURCHASE')], default='CASH', max_length=255),
            preserve_default=False,
        ),
    ]
