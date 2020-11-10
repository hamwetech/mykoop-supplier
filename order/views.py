# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xlrd
import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from conf.utils import log_debug, log_error, genetate_uuid4
from supplier.models import Supplier, Item
from agrodealer.models import AgroDealer, AgroDealerItem
from order.models import SupplyOrder, OrderItem, CustomerOrder, CustomerOrderItem, Customer
from order.forms import OrderItemForm, SupplyOrderForm, CustomerOrderItemForm, CustomerOrderForm, CustomerForm


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_order', '__order']
        context['title'] = 'Agro Dealer'
        context.update(self.extra_context)
        return context
    

class CustomerListView(ExtraContext, ListView):
    model = Customer
    

class CustomerCreateView(ExtraContext, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('order:order_create')
    
    def form_valid(self, form):
        form.instance.customer_reference = genetate_uuid4()
        form.instance.created_by = self.request.user
        # form.send_email()
        return super(CustomerCreateView, self).form_valid(form)


class SupplyOrderListView(ExtraContext, ListView):
    model = SupplyOrder
    
    def get_queryset(self):
        qs = super(SupplyOrderListView, self).get_queryset()
        if self.request.user.profile.access_level.name == "SUPPLIER":
            qs = qs.filter(supplier=self.request.user.supplier_user.supplier)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(SupplyOrderListView, self).get_context_data(**kwargs)
        return context
    

class SupplyOrderCreateView(ExtraContext, View):
    
    template_name = "order/supplyorder_form.html"
    
    def get(self, request, *args, **kwargs):
        initial = {'request': request}
        form = SupplyOrderForm(request = request)
        data = {
            'form': form,
            'item_form': OrderItemForm,
            'active': ['_order', '__order']
        }
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        initial = {'request': self.request}
        form = SupplyOrderForm(request.POST, request = request)
        data = dict()
        error = dict()
        log_debug('GGGG')
        try:
            if form.is_valid():
                with transaction.atomic():
                    x = datetime.datetime.now()
                    order_count = SupplyOrder.objects.all().count()
                    cnt = "%04d" % order_count
                    y = x.strftime("%y")
                    m = x.strftime("%m")
                    order_number = "%s/%s%s" % (cnt,m,y)
                    order = form.save(commit=False)
                    order.created_by = request.user
                    order.order_reference = genetate_uuid4()
                    order.order_number = order_number
                    if request.user.profile.access_level.name == "SUPPLIER":
                        order.supplier = request.user.supplier_user.supplier
                    order.save()
                    
                    data = request.POST
                    item_id = data.getlist('item_id')
                    unit_price = data.getlist('unit_price')
                    quantity = data.getlist('item_quantity')
                    total_price = data.getlist('total_price')
                    
                    for i in range(len(item_id)):

                        OrderItem.objects.create(
                            order = order,
                            item = get_object_or_404(Item, pk=item_id[i]),
                            quantity = quantity[i],
                            unit_price = unit_price[i],
                            price = total_price[i],
                            created_by = request.user
                        )
                    return redirect('order:list')
                
        except Exception as e:
            log_error()
            error['errors'] = "Error %s" % e
            
        data = {
            'form': form,
            'item_form': OrderItemForm,
            'active': ['_order', '__order']
        }
        data.update(error)
        return render(request, self.template_name, data)


class SupplyOrderDetailView(ExtraContext, DetailView):
    model = SupplyOrder
    

def update_status(request):
    pk = request.POST.get('id')
    status = request.POST.get('status')
    print(pk)
    print(status)
    SupplyOrder.objects.filter(pk=pk).update(status=status)
    data = {
        'status': 'success'
    }
    return JsonResponse(data)


class CustomerOrderListView(ExtraContext, ListView):
    model = CustomerOrder
    

class CustomerOrderCreateView(ExtraContext, View):
    
    template_name = "order/customerorder_form.html"
    
    def get(self, request, *args, **kwargs):
        form = CustomerOrderForm()
        data = {
            'form': form,
            'item_form': CustomerOrderItemForm,
            'active': ['_order', '__customer_order']
        }
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        form = CustomerOrderForm(request.POST)
        data = dict()
        error = dict()
        log_debug('GGGG')
        try:
            if form.is_valid():
                with transaction.atomic():
                    x = datetime.datetime.now()
                    order_count = CustomerOrder.objects.all().count()
                    cnt = "%04d" % order_count
                    y = x.strftime("%y")
                    m = x.strftime("%m")
                    order_number = "%s/%s%s" % (cnt,m,y)
                    order = form.save(commit=False)
                    order.created_by = request.user
                    order.order_reference = genetate_uuid4()
                    order.order_number = order_number
                    order.order_date = x
                    order.save()
                    
                    data = request.POST
                    item_id = data.getlist('item_id')
                    unit_price = data.getlist('unit_price')
                    quantity = data.getlist('item_quantity')
                    total_price = data.getlist('total_price')
                    
                    for i in range(len(item_id)):

                        CustomerOrderItem.objects.create(
                            order = order,
                            item = get_object_or_404(AgroDealerItem, pk=item_id[i]),
                            quantity = quantity[i],
                            unit_price = unit_price[i],
                            price = total_price[i],
                            created_by = request.user,
                            order_date = x
                        )
                    return redirect('order:order_list')
                
        except Exception as e:
            log_error()
            error['errors'] = "Error %s" % e
            
        data = {
            'form': form,
            'item_form': OrderItemForm,
            'active': ['_order', '__customer_order']
        }
        data.update(error)
        return render(request, self.template_name, data)


class CustomerOrderDetailView(ExtraContext, DetailView):
    model = CustomerOrder
    

def update_customer_order_status(request):
    pk = request.POST.get('id')
    status = request.POST.get('status')
    print(request.POST)
    CustomerOrder.objects.filter(pk=pk).update(status=status)
    data = {
        'status': 'success'
    }
    return JsonResponse(data)



