# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-27 00:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agrodealer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agrodealer',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agrodealer',
            name='logo',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='supplier/logo/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agrodealer',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
