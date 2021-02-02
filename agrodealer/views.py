# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xlrd

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from conf.utils import log_debug, log_error, genetate_uuid4
from agrodealer.models import AgroDealer, AgroDealerUser, AgroDealerCategory, AgroDealerItem, AgroDealerCategory
from agrodealer.forms import AgroDealerForm, AgroDealerCategoryForm, AgroDealerCategoryForm, AgroDealerItemForm
from userprofile.models import Profile, AccessLevel
from userprofile.forms import UserProfileForm, UserForm
from django.contrib.auth.models import User


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_agrodealer', '__agrodealer']
        context['title'] = 'Agro Dealer'
        context.update(self.extra_context)
        return context
    

class AgroDealerListView(ExtraContext, ListView):
    model = AgroDealer
    
    def get_queryset(self):
        qs = super(AgroDealerListView, self).get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "AGRODEALER":
                qs = qs.filter(agrodealer=self.request.user.agro_dealer_user.agrodealer)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AgroDealerListView, self).get_context_data(**kwargs)
        return context
    
    
class AgroDealerCreateView(ExtraContext, CreateView):
    model = AgroDealer
    form_class = AgroDealerForm
    success_url = reverse_lazy('agrodealer:list')
    

class AgroDealerUpdateView(ExtraContext, UpdateView):
    model = AgroDealer
    form_class = AgroDealerForm
    success_url = reverse_lazy('agrodealer:list')


class AgroDealerUserListView(ExtraContext, ListView):
    model = AgroDealerUser
    extra_context = {'active': ['_agrodealer', '_agrodealer']}
    
    def get_context_data(self, **kwargs):
        context = super(AgroDealerUserListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('agrodealer')
        context['agrodealer_id'] = pk
        return context
    

class AgroDealerUserCreate(View):
    template_name = 'agrodealer/agrodealer_user_form.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        agrodealer = self.kwargs.get('agrodealer')
        instance = None
        profile = None
        coop_admin = None
        if pk:
            user = User.objects.get(pk=pk)
            if user:
                instance = user
                profile = instance.profile
                if hasattr(instance, 'cooperative_admin'):
                    coop_admin = instance.cooperative_admin

        user_form = UserForm(instance=instance)
        profile_form = UserProfileForm(instance=profile)

        data = {'user_form': user_form, 'profile_form': profile_form, 'supplier_id': pk, 'active': ['_agrodealer']}
        return render(request, self.template_name, data)

    def post(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        agrodealer = self.kwargs.get('agrodealer')
        instance = None
        errors = dict()

        if pk:
            instance = User.objects.filter(pk=pk)
            if instance.exists():
                instance = instance[0]
                profile = instance.profile
                if hasattr(instance, 'cooperative_admin'):
                    coop_admin = instance.cooperative_admin
        user_form = UserForm(request.POST, instance=instance)
        profile_form = UserProfileForm(request.POST, instance=instance)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    if not errors:
                        user = user_form.save(commit=False);
                        if not instance:
                            user.set_password(user.password)
                        user.save()
                        profile_form = UserProfileForm(request.POST, instance=user.profile)
                        profile_form.save(commit=False)
                        profile_form.access_level = get_object_or_404(AccessLevel, name='AGRODEALER')
                        profile_form.save()
                        
                        inst_s = AgroDealer.objects.get(pk=agrodealer)
                        AgroDealerUser.objects.create(agrodealer=inst_s, user=user, )
                        return redirect('agrodealer:agrodealer_user', agrodealer=agrodealer)
            except Exception as e:
                log_error()
                errors['errors'] = "Error %s" % e
        data = {'user_form': user_form, 'profile_form': profile_form, 'active': ['_agrodealer']}
        data.update(errors)
        return render(request, self.template_name, data)
    
    

class AgroDealerCategoryCreateView(ExtraContext, CreateView):
    model = AgroDealerCategory
    form_class = AgroDealerCategoryForm
    extra_context = {'active': ['_union_prod', '_agrodealer_items']}
    success_url = reverse_lazy('agrodealer:category_list')


class AgroDealerCategoryUpdateView(ExtraContext, UpdateView):
    model = AgroDealerCategory
    form_class = AgroDealerCategoryForm
    extra_context = {'active': ['_agrdealer', '_agrodealer_items']}
    success_url = reverse_lazy('agrodealer:category_list')


class AgroDealerCategoryListView(ExtraContext, ListView):
    model = AgroDealerCategory
    extra_context = {'active': ['_union_prod', '_agrodealer_items']}

    def get_queryset(self):
        qs = super(AgroDealerCategoryListView, self).get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "AGRODEALER":
                qs = qs.filter(agrodealer=self.request.user.agro_dealer_user.agrodealer)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AgroDealerCategoryListView, self).get_context_data(**kwargs)
        return context


class AgroDealerItemCreateView(ExtraContext, CreateView):
    model = AgroDealerItem
    form_class = AgroDealerItemForm
    extra_context = {'active': ['_union_prod', '_agrodealer_items']}
    success_url = reverse_lazy('agrodealer:item_list')

    def get_form_kwargs(self):
        kwargs = super(AgroDealerItemCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class AgroDealerItemUpdateView(ExtraContext, UpdateView):
    model = AgroDealerItem
    form_class = AgroDealerItemForm
    extra_context = {'active': ['_union_prod', '_agrodealer_items']}
    success_url = reverse_lazy('agrodealer:item_list')


class AgroDealerItemListView(ExtraContext, ListView):
    model = AgroDealerItem
    extra_context = {'active': ['_union_prod', '_agrodealer_items']}

    def get_queryset(self):
        qs = super(AgroDealerItemListView, self).get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == "AGRODEALER":
                print(self.request.user.agro_dealer_user.agrodealer)
                qs = qs.filter(agrodealer=self.request.user.agro_dealer_user.agrodealer)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AgroDealerItemListView, self).get_context_data(**kwargs)
        return context


def get_agrodealeritem_price(request, pk):
    try:
        pp = AgroDealerItem.objects.get(pk=pk)
        return JsonResponse({"id": pp.id, "name": pp.name, "price": pp.price}, safe=False)
    except Exception as e:
        log_error()
        return JsonResponse({"price": "error"})

