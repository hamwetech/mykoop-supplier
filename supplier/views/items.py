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
from ..models import Supplier, SupplierUser, Item
from ..forms import SupplierForm, ItemForm

from django.contrib.auth.models import User

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_supplier']
        context['title'] = 'Supplier'
        context.update(self.extra_context)
        return context


class ItemCreateView(ExtraContext, CreateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['_union_prod', '__Item']}
    success_url = reverse_lazy('supplier:item_list')


class ItemUpdateView(ExtraContext, UpdateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['_union_prod', '__Item']}
    success_url = reverse_lazy('supplier:item_list')


class ItemListView(ExtraContext, ListView):
    model = Item
    extra_context = {'active': ['_union_prod', '__Item']}


def get_item_price(request, pk):
    try:
        pp = Item.objects.get(pk=pk)
        return JsonResponse({"price": pp.price})
    except Exception:
        return JsonResponse({"price": "error"})

