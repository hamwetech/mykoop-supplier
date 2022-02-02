# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from supplier.models import Supplier


class Transaction(models.Model):
    supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE)
    date_initiated = models.DateTimeField()
    transaction_reference = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=16,
                                      choices=(('CASH', 'CASH'), ('BANK', 'BANK'), ('MOBILE MONEY', 'MOBILE MONEY')))
    status = models.CharField(max_length=15,
                              choices=(('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')),
                              blank=True)
    balance_before = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    balance_after = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    request = models.TextField()
    response = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField()
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "member_payment_transaction"

    def __unicode__(self):
        return "%s" % self.transaction_reference



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
