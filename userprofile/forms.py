from django import forms
from django.contrib.auth.models import User, Group

from conf.utils import bootstrapify
from userprofile.models import *

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)

        super(UserForm, self).__init__(instance=instance, *args, **kwargs)
        if instance:
            self.fields.pop('password')
            self.fields.pop('confirm_password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'username', 'password', 'confirm_password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['msisdn', 'access_level']
        

# class UserProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         
#         self.user = kwargs['instance'].user if kwargs['instance'] else None
#         user_kwargs = kwargs.copy()
#         user_kwargs['instance'] = self.user
#         self.user_form = UserForm(*args, **user_kwargs)
#         
#         super(UserProfileForm, self).__init__(*args, **kwargs)
# 
#         self.fields.update(self.user_form.fields)
#         self.initial.update(self.user_form.initial)
#         
#     def save(self, *args, **kwargs):
#         self.user_form.save(*args, **kwargs)
#         return super(UserProfileForm, self).save(*args, **kwargs)
# 
#     class Meta:
#         model = Profile
#         fields = ['msisdn', 'access_level']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class AccessLevelForm(forms.ModelForm):
    class Meta:
        model = AccessLevel
        fields = ['name']
        

class AccessLevelGroupForm(forms.ModelForm):
    class Meta:
        model = AccessLevelGroup
        fields = ['access_level', 'group']
        
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=254, widget=forms.PasswordInput())

     
bootstrapify(LoginForm)
bootstrapify(AccessLevelForm)    
bootstrapify(AccessLevelGroupForm)    
bootstrapify(GroupForm)    
bootstrapify(UserForm)
bootstrapify(UserProfileForm)
