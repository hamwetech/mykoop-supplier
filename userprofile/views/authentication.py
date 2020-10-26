# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from conf.utils import log_error, log_debug
from userprofile.models import *
from userprofile.forms import GroupForm, AccessLevelForm, AccessLevelGroupForm, LoginForm


class GroupCreateView(CreateView):
    model = Group
    # template_name = "conf/group_form.html"
    form_class = GroupForm
    success_url = reverse_lazy('profile:group_list')


class GroupUpdateView(UpdateView):
    model = Group
    # template_name = "conf/group_form.html"
    form_class = GroupForm
    success_url = reverse_lazy('conf:group_list')
    
    
class GroupListView(ListView):
    model = Group
    

class AccessLevelListView(ListView):
    model = AccessLevel


class AccessLevelCreateView(CreateView):
    model = AccessLevel
    form_class = AccessLevelForm
    success_url = reverse_lazy('profile:access_list')
    

class AccessLevelUpdateView(UpdateView):
    model = AccessLevel
    form_class = AccessLevelForm
    success_url = reverse_lazy('profile:access_list')
    


class AccessLevelGroupListView(ListView):
    model = AccessLevelGroup
    
 
class AccessLevelGroupCreateView(CreateView):
    model = AccessLevelGroup
    form_class = AccessLevelGroupForm
    success_url = reverse_lazy('profile:ag_list')
    

class AccessLevelGroupUpdateView(UpdateView):
    model = AccessLevelGroup
    form_class = AccessLevelGroupForm
    success_url = reverse_lazy('profile:ag_list')


class ChangePasswordView(View):

    template_name = 'userprofile/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('new_password2')
            check = password_log(request.user, password)
            if check:
                user = form.save()
                data = {
                    'title': 'Password Change',
                    'status_message': 'Your Password has been updated successfully.'
                }
                messages.success(request, 'Password Updated successfully')
                return render(request, 'account/status.html', data)
            messages.error(request, 'Sorry password Denied. Please use a password different from your previous %s passwords' % system_settings.password_reuse_threshold)
        return render(request, self.template_name, {'form': form})


class AdminChangePasswordView(View):

    template_name = 'userprofile/change_password.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        form = SetPasswordForm(user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        __user = User.objects.get(pk=pk)
        form = SetPasswordForm(__user, request.POST)

        if form.is_valid():
           user = form.save()
           data = {
                'title': 'Password Change',
                'status_message': 'Your Password has been updated successfully.'
           }
           messages.success(request, 'Password Updated successfully')
           return redirect('profile:user_list')
            #messages.success(request, 'Password Updated successfully')
            # return render(request, 'account/status.html', data)
            #return redirect('profile:user_list')
            #messages.error(request, 'Sorry password Denied. Please use a password different from your previous %s passwords' % system_settings.password_reuse_threshold)
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = "userprofile/login.html"
    
    def get(self, request, *args, **kwargs):
        data = {"form": LoginForm}
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        data = dict()
        form = LoginForm(request.POST)
        cooperative = False
        try:
           if form.is_valid():
                # set_login_attempt(request)
                username = form.cleaned_data.get('username', '')
                password = form.cleaned_data.get('password', '')

                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        data['errors'] = "Your account is inactive"
                else:
                    data['errors'] = "Username or Password invalid"
            
        except Exception as e:
            data['errors'] = "Login Error. Contact Admin"
            print (e)
            log_error()
        return render(request, self.template_name, {'form': form, 'errors': data, 'active': ['staff_login', 'setting']})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
        #return super(LogoutView, self).get(request, *args, **kwargs)
    
    