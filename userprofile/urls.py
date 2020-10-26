from django.conf.urls import url

from userprofile.views.authentication import *
from userprofile.views.user_managment import *

urlpatterns = [
    url(r'access/group/list/$', AccessLevelGroupListView.as_view(), name='ag_list'),
     url(r'access/group/create/$', AccessLevelGroupCreateView.as_view(), name='ag_create'),
     url(r'access/group/(?P<pk>[\w]+)/$', AccessLevelGroupUpdateView.as_view(), name='ag_edit'),
     url(r'access/list/$', AccessLevelListView.as_view(), name='access_list'),
     url(r'access/create/$', AccessLevelCreateView.as_view(), name='access_create'),
     url(r'access/(?P<pk>[\w]+)/$', AccessLevelUpdateView.as_view(), name='access_edit'),
     url(r'group/list/$', GroupListView.as_view(), name='group_list'),
     url(r'group/create/$', GroupCreateView.as_view(), name='group_create'),
     url(r'group/(?P<pk>[\w]+)/$', GroupUpdateView.as_view(), name='group_edit'),
     url(r'password/change/$', ChangePasswordView.as_view(), name='password_edit'),
     url(r'password/change/(?P<pk>[\w]+)/$', AdminChangePasswordView.as_view(), name='admin_password_edit'),
     url(r'create/$', UserProfileCreateView.as_view(), name='user_create'),
     url(r'list/$', UserProfileListView.as_view(), name='user_list'),
     url(r'(?P<pk>[\w]+)/$', UserProfileCreateView.as_view(), name='user_edit'),
    ]