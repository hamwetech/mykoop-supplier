# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-29 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220123_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='transaction_type',
            field=models.CharField(choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], default='CREDIT', max_length=20),
            preserve_default=False,
        ),
    ]
