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


class SupplyOrder(models.Model):
    member_id = models.CharField(max_length=255, blank=True)
    order_reference = models.CharField(max_length=255, blank=True)
    order_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=255, default='PENDING')
    order_date = models.DateTimeField()
    accept_date = models.DateTimeField(null=True, blank=True)
    reject_date = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=120, null=True, blank=True)
    ship_date = models.DateTimeField(null=True, blank=True)
    delivery_accept_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_reason = models.CharField(max_length=120, null=True, blank=True)
    collect_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supply_order'

    def __unicode__(self):
        return "%s" % self.order_reference or u''

    def get_orders(self):
        return OrderItem.objects.filter(order=self)


class OrderItem(models.Model):
    order = models.ForeignKey(SupplyOrder, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supply_order_item'

    def __unicode__(self):
        return "%s" % self.item or u''
