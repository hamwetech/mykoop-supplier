import xlrd

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from conf.utils import log_debug, log_error
from ..models import Supplier, SupplierUser, Item, Category
from ..forms import SupplierForm, ItemForm, CategoryForm

from django.contrib.auth.models import User

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['__item']
        context['title'] = 'Item'
        context.update(self.extra_context)
        return context
    

class CategoryCreateView(ExtraContext, CreateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'active': ['_union_prod', '__category']}
    success_url = reverse_lazy('supplier:category_list')


class CategoryUpdateView(ExtraContext, UpdateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'active': ['_union_prod', '__category']}
    success_url = reverse_lazy('supplier:category_list')


class CategoryListView(ExtraContext, ListView):
    model = Category
    extra_context = {'active': ['_union_prod', '__category']}    


class ItemCreateView(ExtraContext, CreateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['_union_prod', '__item']}
    success_url = reverse_lazy('supplier:item_list')


class ItemUpdateView(ExtraContext, UpdateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['_union_prod', '__item']}
    success_url = reverse_lazy('supplier:item_list')


class ItemListView(ExtraContext, ListView):
    model = Item
    extra_context = {'active': ['_union_prod', '__item']}
    
    def get_queryset(self):
        qs = super(ItemListView, self).get_queryset()
        if self.request.user.profile.access_level.name == "SUPPLIER":
            qs = qs.filter(supplier=self.request.user.supplier_user.supplier)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        return context


def get_item_price(request, pk):
    try:
        pp = Item.objects.get(pk=pk)
        return JsonResponse({"id": pp.id, "name": pp.name, "price": pp.price}, safe=False)
    except Exception as e:
        log_error()
        return JsonResponse({"price": "error"})

