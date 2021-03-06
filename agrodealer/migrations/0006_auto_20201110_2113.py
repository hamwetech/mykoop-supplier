# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-11-10 18:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0005_auto_20201110_1759'),
        ('agrodealer', '0005_auto_20201030_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='agrodealer',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier'),
        ),
        migrations.AlterField(
            model_name='agrodealeruser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agro_dealer_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
