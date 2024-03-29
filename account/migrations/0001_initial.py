# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-01-23 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reference', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='AccountTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_before', models.DecimalField(decimal_places=2, max_digits=9)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('balance_after', models.DecimalField(decimal_places=2, max_digits=9)),
                ('request_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED'), ('UNKNOWN', 'UNKNOWN')], default='PENDING', max_length=62)),
                ('category', models.CharField(choices=[('ORDER PAYMENT', 'ORDER PAYMENT')], max_length=120)),
                ('request', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('response_date', models.DateTimeField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
    ]
