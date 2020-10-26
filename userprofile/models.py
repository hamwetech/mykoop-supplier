# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token


class AccessLevel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'access_level'
    
    def __unicode__(self):
        return self.name
    

class AccessLevelGroup(models.Model):
    access_level = models.OneToOneField(AccessLevel, unique=True)
    group = models.ManyToManyField(Group)
    
    class Meta:
        db_table = 'access_levell_group'
    
    def __unicode__(self):
        return "%s" % self.access_level


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    msisdn = models.CharField(max_length=12, unique=True, null=True, blank=True)
    access_level = models.ForeignKey(AccessLevel, null=True, blank=True, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=0)
    receive_sms_notifications = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'user_profile'
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()                           
                                    
