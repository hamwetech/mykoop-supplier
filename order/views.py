# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xlrd
import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from conf.utils import log_debug, log_error, genetate_uuid4, get_deleted_objects
from supplier.models import Supplier, Item
from agrodealer.models import AgroDealer, AgroDealerItem
from payment.PaymentTransaction import PaymentTransaction
from account.models import Account
from order.models import SupplyOrder, OrderItem, CustomerOrder, CustomerOrderItem, Customer
from order.forms import OrderItemForm, SupplyOrderForm, CustomerOrderItemForm, CustomerOrderForm, CustomerForm, MakePaymentForm
from account.AccountActivity import AccountActivity


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
    extra_context = {'active': ['_order', '_agrodealer_order']}
    

class CustomerCreateView(ExtraContext, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('order:order_create')
    extra_context = {'active': ['_order', '_agrodealer_order']}
    
    def form_valid(self, form):
        form.instance.customer_reference = genetate_uuid4()
        form.instance.created_by = self.request.user
        # form.send_email()
        return super(CustomerCreateView, self).form_valid(form)


class SupplierItemOrderList(ExtraContext, ListView):
    model = OrderItem
    ordering = ['-create_date']

    def get_queryset(self):
        qs = super(SupplierItemOrderList, self).get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "SUPPLIER":
                qs = qs.filter(item__supplier=self.request.user.supplier_user.supplier).exclude(status='PENDING')
        return qs



class SupplyOrderListView(ExtraContext, ListView):
    model = SupplyOrder
    ordering = ['-create_date']
    def get_queryset(self):
        qs = super(SupplyOrderListView, self).get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "SUPPLIER":
                qs = qs.filter(supplier=self.request.user.supplier_user.supplier)
            if self.request.user.profile.access_level.name == "AGRODEALER":
                qs = qs.filter(agro_dealer=self.request.user.agro_dealer_user.agrodealer)
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
                    if not request.user.is_superuser:
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
                    if order.payment_mode == "MOBILE MONEY":
                        redirect('order:order_payment',order.id)
                    return redirect('order:detail', order.id)
                
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
    

class SupplyOrderDeleteView(ExtraContext, DeleteView):
    model = SupplyOrder
    success_url = reverse_lazy('order:list')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        #
        context = super(SupplyOrderDeleteView, self).get_context_data(**kwargs)
        #

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        #
        return context


def update_status(request):
    pk = request.POST.get('id')
    status = request.POST.get('status')
    try:
        ss = SupplyOrder.objects.get(pk=pk)
        if status == "MAKEPAYMENT":
            msisdn = ss.agro_dealer.phone_number
            amount = ss.order_price
            pmt = PaymentTransaction(msisdn, amount)
            pmt.mobile_money_transation()
            status = "PENDING PAYMENT"
        ss.status=status
        ss.save()
        OrderItem.objects.filter(order=ss.id).update(status="CONFIRMED")
        data = {'status': 'success'}
    except Exception as e:
        data = {"status": "error"}
        print(e)
    return JsonResponse(data)


def update_item_status(request):
    pk = request.POST.get('id')
    status = request.POST.get('status')
    try:
        ss = OrderItem.objects.get(pk=pk)
        so = SupplyOrder.objects.get(pk=ss.order.pk)
        if status == "MAKEPAYMENT":
            msisdn = ss.agro_dealer.phone_number
            amount = ss.order_price
            pmt = PaymentTransaction(msisdn, amount)
            pmt.mobile_money_transation()
            status = "PENDING PAYMENT"
        ss.status=status
        ss.save()
        print(ss)
        # so.status = "PROCESSING"
        c = OrderItem.objects.filter(order=ss.order, status='PENDING')
        if not c.exists():
            so.status = "CONFIRMED"
        so.save()

        data = {'status': 'success'}
    except Exception as e:
        data = {"status": "error"}
        print(e)
    return JsonResponse(data)


class CustomerOrderListView(ExtraContext, ListView):
    model = CustomerOrder
    extra_context = {'active': ['_order', '_agrodealer_order']}
    

class CustomerOrderCreateView(ExtraContext, View):
    
    template_name = "order/customerorder_form.html"
    
    def get(self, request, *args, **kwargs):
        form = CustomerOrderForm()
        data = {
            'form': form,
            'item_form': CustomerOrderItemForm,
            'active': ['_order', '_agrodealer_order']
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
            'active': ['_order', '_agrodealer_order']
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


def load_supplier_items(request):
    supplier = request.GET.get('supplier')
    items = Item.objects.values('id', 'name').filter(supplier__id=supplier).order_by('name')
    return JsonResponse(list(items), safe=False)


class OrderPaymentView(FormView):
    form_class = MakePaymentForm
    template_name = "order/order_payment.html"
    success_url = reverse_lazy('order:list')

    def form_valid(self, form):
        order_pk = self.kwargs.get('pk')
        msisdn = form.cleaned_data.get('phone_number')
        try:
            with transaction.atomic():
                order = get_object_or_404(SupplyOrder, pk=order_pk)
                amount = order.order_price
                account = Account.objects.get(is_holding=True)
                pmt = PaymentTransaction(account, msisdn, amount)
                res = pmt.mobile_money_transation(order.order_number, 'ORDER PAYMENT')
                print(res)
                status = "PENDING PAYMENT"
                if res.get('status') == "FAILED":
                    status = "PENDING"
                    order.remark = "Mobile Money Transaction Failed"
                if res.get('status') == "SUCCESSFUL":
                    status = "PENDING"
                    order.remark = "Payment made successfully"
                    order.is_paid = True
                    acc_act = AccountActivity(account)
                    acc_act.credit_account(amount)
                    order.payment_date = datetime.datetime.now()
                order.status = status
                order.save()
        except Exception as e:
            log_error()
        return super(OrderPaymentView, self).form_valid(form)

    def form_invalid(self, form):
        return super(OrderPaymentView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderPaymentView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(SupplyOrder, pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('order:detail',
                       kwargs={
                           'pk': self.kwargs.get('pk'),
                       })