# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MobileMoneyRequest(models.Model):
    transaction_reference = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    origin = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=(('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')), blank=True)
    request = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mobile_money_request"
        
    def __unicode__(self):
        return self.phone_number
