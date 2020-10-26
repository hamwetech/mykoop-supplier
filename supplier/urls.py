from django.conf.urls import url

from supplier.views.items import *
from supplier.views.supplier import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierUserListView, SupplierUserCreate

urlpatterns = [
    url(r'item/price/(?P<pk>[\w]+)/$', get_item_price, name='item_price'),
    url(r'item/edit/(?P<pk>[\w]+)/$', ItemUpdateView.as_view(), name='item_update'),
    url(r'item/list/$', ItemListView.as_view(), name='item_list'),
    url(r'item/create/$', ItemCreateView.as_view(), name='item_create'),
    url(r'(?P<supplier>[\w]+)/users/$', SupplierUserListView.as_view(), name='supplier_user'),
    url(r'(?P<supplier>[\w]+)/users/add/$', SupplierUserCreate.as_view(), name='supplier_user_add'),
    url(r'list/$', SupplierListView.as_view(), name='supplier_list'),
    url(r'add/$', SupplierCreateView.as_view(), name='supplier_create'),
    url(r'edit/(?P<pk>[\w]+)/$', SupplierUpdateView.as_view(), name='supplier_edit'),



]