from django.conf.urls import url
from apiv1.views import *

urlpatterns = [
    url(r'items/list/$', ItemsListView.as_view(), name='item_list'),
    url(r'items/list/(?P<order>[-\w]+)/$', ItemsListView.as_view(), name='item_list'),

 ]