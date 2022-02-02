# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from conf.models import County, District, SubCounty
from account.models import Account


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='supplier/logo/', null=True, blank=True,)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=Supplier)
def create_account(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(name=instance.name)
        instance.account = account
        instance.save()


@receiver(post_save, sender=Supplier)
def save_account(sender, instance, **kwargs):
    if not instance.account:
        account = Account.objects.create(name=instance.name)
        instance.account = account
        instance.save()

class SupplierUser(models.Model):
    supplier = models.ForeignKey(Supplier)
    user = models.OneToOneField(User, related_name='supplier_user')
    class Meta:
        db_table = 'supplier_user'


class Category(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    supplier_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    mark_up_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'

    def __unicode__(self):
        return "%s - %s" % (self.name, self.supplier)


