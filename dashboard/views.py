# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Value as V
from django.db.models.functions import Concat
from collections import Counter
from supplier.models import *
from agrodealer.models import *
from order.models import *

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        suppliers = Supplier.objects.all()
        agro_dealer = AgroDealer.objects.all()
        supplier_orders = SupplyOrder.objects.all()
        customer_orders = CustomerOrder.objects.all()
        order_items = CustomerOrderItem.objects.all()
        
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "SUPPLIER":
                supplier_orders = supplier_orders.filter(supplier=self.request.user.supplier_user.supplier)
            if self.request.user.profile.access_level.name == "AGRODEALER":
                supplier_orders = supplier_orders.filter(agro_dealer=self.request.user.agro_dealer_user.agrodealer)
                order_items = order_items.filter(item__agrodealer=self.request.user.agro_dealer_user.agrodealer)
        context['suppliers'] = suppliers.count()
        context['agro_dealers'] = agro_dealer.count()
        context['supplier_orders'] = supplier_orders
        context['order_items'] = order_items
        return context
    
    


