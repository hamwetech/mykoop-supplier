# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-27 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrodealer', '0002_auto_20201027_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agrodealer',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='supplier/logo/'),
        ),
    ]
