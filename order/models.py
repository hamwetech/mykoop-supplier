# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from agrodealer.models import AgroDealer, AgroDealerItem
from supplier.models import Supplier, Item
from django.contrib.auth.models import User


class Customer(models.Model):
    customer_reference = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "customer"
        
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.phone_number)
        
class SupplyOrder(models.Model):
    status = (
        ('PENDING', 'PENDING'),
        ('CONFIRMED', 'CONFIRMED'),
        ('CANCELLED', 'CANCELLED'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('REJECTED', 'REJECTED'),
    )
    agro_dealer = models.ForeignKey(AgroDealer, blank=True)
    supplier = models.ForeignKey(Supplier, blank=True)
    order_number = models.CharField(max_length=255, blank=True)
    order_reference = models.CharField(max_length=255, blank=True)
    order_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=255, choices=status, default='PENDING')
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
    item = models.ForeignKey(Item, blank=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, blank=True, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supply_order_item'

    def __unicode__(self):
        return "%s" % self.item or u''
    

class CustomerOrder(models.Model):
    status = (
        ('PENDING', 'PENDING'),
        ('CONFIRMED', 'CONFIRMED'),
        ('CANCELLED', 'CANCELLED'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('REJECTED', 'REJECTED'),
    )
    agro_dealer = models.ForeignKey(AgroDealer, blank=True, null=True)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True)
    order_reference = models.CharField(max_length=255, blank=True)
    order_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=255, choices=status, default='PENDING')
    order_date = models.DateTimeField()
    accept_date = models.DateTimeField(null=True, blank=True)
    reject_date = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=120, null=True, blank=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer_order'

    def __unicode__(self):
        return "%s" % self.order_reference or u''

    def get_orders(self):
        return CustomerOrderItem.objects.filter(order=self)


class CustomerOrderItem(models.Model):
    status = (
        ('PENDING', 'PENDING'),
        ('CONFIRMED', 'CONFIRMED'),
        ('CANCELLED', 'CANCELLED'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('REJECTED', 'REJECTED'),
    )
    order = models.ForeignKey(CustomerOrder, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(AgroDealerItem, blank=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, blank=True, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    status = models.CharField(max_length=255, choices=status, default='PENDING')
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
        db_table = 'customer_order_item'

    def __unicode__(self):
        return "%s" % self.item or u''