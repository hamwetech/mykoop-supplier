# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class AgroDealer(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    
    class Meta:
        db_table = "agro_dealer"
