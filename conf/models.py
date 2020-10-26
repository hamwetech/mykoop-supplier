# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class District(models.Model):
    name = models.CharField(max_length=50, unique=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'district'
        
    def __unicode__(self):
        return self.name
    

class County(models.Model):
    district = models.ForeignKey(District)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'county'
        unique_together = ('district', 'name')
    
    def __unicode__(self):
        return self.name
    
    
class SubCounty(models.Model):
    county = models.ForeignKey(County)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sub_county'
        unique_together = ['county', 'name']
    
    def __unicode__(self):
        return self.name
    
    
class Parish(models.Model):
    sub_county = models.ForeignKey(SubCounty)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parish'
        unique_together = ['sub_county', 'name']
    
    def __unicode__(self):
        return self.name
    

class Village(models.Model):
    parish = models.ForeignKey(Parish)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'village'
        
    def __unicode__(self):
        return self.name
 
    
class PaymentMethod(models.Model):
    method = models.CharField('Method', max_length=50)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_method'
        
    def __unicode__(self):
        return self.method
    
    
class SystemSettings(models.Model):
    send_message = models.BooleanField(default=0)
    mobile_money_payment = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'system_settings'
        
    def __unicode__(self):
        return u'Settings'
    

class MessageTemplates(models.Model):
    collection =  models.TextField(null=True, blank=True)
    coop_share_purchase = models.TextField(null=True, blank=True)
    member_share_purchase  = models.TextField(null=True, blank=True)
    member_registration = models.TextField(null=True, blank=True)
    purchase_confirmation = models.TextField(null=True, blank=True)
    payment_confirmation = models.TextField(null=True, blank=True)
    supply_request = models.TextField(null=True, blank=True)
    supply_confirmation = models.TextField(null=True, blank=True)
    supply_cancelled = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'message_template'
        
    def __unicode__(self):
        return u'Messages Template'
