# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)

    class Meta:
        db_table = "organisation"


class Client(models.Model):
    organisation = models.ForeignKey(Organisation, null=True, blank=True, on_delete=model.SET_NULL)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "client"

