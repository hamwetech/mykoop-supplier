# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-29 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_accounttransaction_internal_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='provider_reference',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
