# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-29 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_accounttransaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='internal_reference',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
