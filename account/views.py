# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from account.models import AccountTransaction
from account.forms import TransactionSearchForm


class AccountTransactionListView(ListView):
    model = AccountTransaction
    ordering = ['-id']

    def get_queryset(self):
        queryset = super(AccountTransactionListView, self).get_queryset()
        search = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(Q(reference__icontains=search) | Q(internal_reference__icontains=search) | Q (phone_number__icontains=search)| Q (provider_reference__icontains=search))
        if start_date:
            queryset = queryset.filter(create_date=start_date)
        if start_date and end_date:
            queryset = queryset.filter(create_date__gte=start_date, create_date__lte=end_date)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AccountTransactionListView, self).get_context_data(**kwargs)
        context['form'] = TransactionSearchForm
        return context


class AccountTransactionDetailView(DetailView):
    model = AccountTransaction
