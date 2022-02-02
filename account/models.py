# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True)
    reference = models.CharField(max_length=255)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    is_holding = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:  # to ensure that the object is being updated and is not a new one
            if not self.is_holding:
                check_active_uniquniess = self._meta.model.objects.filter(name=self.name).exclude(id=self.id).count()
                if check_active_uniquniess:
                    raise ValidationError(
                        "Holding account already exists!")
        super(Account, self).save(*args, **kwargs)


class AccountTransaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('PROCESSING', 'PROCESSING'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
        ('FAILED', 'FAILED'),
        ('UNKNOWN', 'UNKNOWN'),
    )
    account = models.ForeignKey(Account)
    reference = models.CharField(max_length=255, unique=True, null=True)
    internal_reference = models.CharField(max_length=255, unique=True, null=True)
    phone_number = models.CharField(max_length=255)
    balance_before = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    balance_after = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    request_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=20, choices=(('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')))
    status = models.CharField(max_length=62, choices=STATUS_CHOICES, default='PENDING')
    category = models.CharField(max_length=120, choices=(('ORDER PAYMENT', 'ORDER PAYMENT'),))
    request = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    provider_reference = models.CharField(max_length=255, unique=True, null=True)
    response_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
