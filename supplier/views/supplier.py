import xlrd

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from conf.utils import log_debug, log_error
from ..models import Supplier, SupplierUser
from ..forms import SupplierForm

from userprofile.models import Profile
from userprofile.forms import UserProfileForm, UserForm
from django.contrib.auth.models import User


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_supplier']
        context['title'] = 'Supplier'
        context.update(self.extra_context)
        return context


class SupplierListView(ExtraContext, ListView):
    model = Supplier
    extra_context = {'active': ['_config', '__district']}


class SupplierCreateView(ExtraContext, CreateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['_supplier', '__spplier']}
    success_url = reverse_lazy('supplier:supplier_list')


class SupplierUpdateView(ExtraContext, UpdateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['_supplier', '__spplier']}
    success_url = reverse_lazy('supplier:supplier_list')


class SupplierUserListView(ExtraContext, ListView):
    model = SupplierUser

    def get_context_data(self, **kwargs):
        context = super(SupplierUserListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('supplier')
        context['supplier_id'] = pk
        return context


class SupplierUserCreate(View):
    template_name = 'supplier/supplier_user_form.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        supplier = self.kwargs.get('supplier')
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

        data = {'user_form': user_form, 'profile_form': profile_form, 'supplier_id': pk}
        return render(request, self.template_name, data)

    def post(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        supplier = self.kwargs.get('supplier')
        instance = None
        profile = None
        errors = dict()

        if pk:
            instance = User.objects.filter(pk=pk)
            if instance.exists():
                instance = instance[0]
                profile = instance.profile
                if hasattr(instance, 'cooperative_admin'):
                    coop_admin = instance.cooperative_admin
        user_form = UserForm(request.POST, instance=instance)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    if not errors:
                        user = user_form.save(commit=False);
                        if not instance:
                            user.set_password(user.password)
                        user.save()
                        profile_form = UserProfileForm(request.POST, instance=user.profile)
                        profile_form.save()
                        inst_s = Supplier.objects.get(pk=supplier)
                        SupplierUser.objects.create(supplier=inst_s, user=user)
                        return redirect('supplier:supplier_user', supplier=supplier)
            except Exception as e:
                log_error()
                errors['errors'] = "Error %s" % e
        data = {'user_form': user_form, 'profile_form': profile_form}
        data.update(errors)
        return render(request, self.template_name, data)