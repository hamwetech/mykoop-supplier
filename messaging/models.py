from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class OutgoingMessages(models.Model):
    msisdn = models.CharField(max_length=12)
    message = models.TextField()
    sent_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    remark = models.CharField(max_length=160, null=True, blank=True)
    sent_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, default='PENDING')
    response = models.TextField(null=True, blank=True)
    update_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "outgoing_message"
    
    def __unicode__(self):
        return self.msisdn
    
