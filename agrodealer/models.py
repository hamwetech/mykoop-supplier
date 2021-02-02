# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from conf.models import County, District, SubCounty
from supplier.models import Supplier

class AgroDealer(models.Model):
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    reference = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='supplier/logo/', null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "agro_dealer"
        
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
    

class AgroDealerUser(models.Model):
    agrodealer = models.ForeignKey(AgroDealer)
    user = models.OneToOneField(User, related_name='agro_dealer_user')
    class Meta:
        db_table = 'agrodealer_user'
    
    def __unicode__(self):
        return self.user.get_full_name()


class AgroDealerCategory(models.Model):
    name = models.CharField(max_length=255)
    agrodealer = models.ForeignKey(AgroDealer, null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "agrodealer_category"
    
    def __unicode__(self):
        return self.name
    

class AgroDealerItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(AgroDealerCategory, on_delete=models.CASCADE)
    agrodealer = models.ForeignKey(AgroDealer, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agrodealer_item'
        unique_together = ['name', 'agrodealer', 'price']

    def __unicode__(self):
        return self.name