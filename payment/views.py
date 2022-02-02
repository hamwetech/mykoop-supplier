# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
import xlwt
import xlrd
import json
from django.utils.encoding import smart_str
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from payment.models import Transaction
from payment.utils import payment_transction
from payment.PaymentTransaction import PaymentTransaction

from conf.utils import generate_alpanumeric, log_debug, log_error

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_payment']
        context.update(self.extra_context)
        return context
    

class TransactionListView(ExtraContext, ListView):
    model = Transaction
    ordering = ['-payment_date']
    extra_context = {'active': ['_payment']}
    
    def get_queryset(self):
        queryset = super(TransactionListView, self).get_queryset()
        
        if not self.request.user.profile.is_union():
            if not self.request.user.profile.is_partner():
                cooperative = self.request.user.cooperative_admin.cooperative 
                queryset = queryset.filter(Q(member__cooperative=cooperative)| Q(cooperative=cooperative))
        
        search = self.request.GET.get('search')
        cooperative = self.request.GET.get('cooperative')
        status = self.request.GET.get('status')
        payment_method = self.request.GET.get('payment_method')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if search:
            queryset = queryset.filter(Q(transaction_reference__icontains=search)|Q(member__first_name__icontains=search)|Q(member__surname__icontains=search)|Q(member__phone_number__icontains=search)|Q(member__member_id__icontains=search))
        if cooperative:
            queryset = queryset.filter(cooperative__id = cooperative)
        if status:
            queryset = queryset.filter(status = status)
        if payment_method:
            queryset = queryset.filter(payment_method = payment_method)
        if start_date and end_date:
            queryset = queryset.filter(payment_date__gte = start_date, payment_date__lte = end_date)
        if start_date:
            queryset = queryset.filter(payment_date = start_date)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(TransactionListView,self).get_context_data(**kwargs)
        return context
