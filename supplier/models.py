# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='supplier/logo/')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'

    def __unicode__(self):
        return self.name


class SupplierUser(models.Model):
    supplier = models.ForeignKey(Supplier)
    user = models.ForeignKey(User)
    class Meta:
        db_table = 'supplier_user'


class Category(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'

    def __unicode__(self):
        return self.name


