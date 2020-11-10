from django.conf.urls import url
from agrodealer.views import *

urlpatterns = [
    
    url(r'category/edit/(?P<pk>[\w]+)/$', AgroDealerCategoryCreateView.as_view(), name='category_update'),
    url(r'category/list/$', AgroDealerCategoryListView.as_view(), name='category_list'),
    url(r'category/create/$', AgroDealerCategoryCreateView.as_view(), name='category_create'),
    url(r'item/list/$', AgroDealerItemListView.as_view(), name='item_list'),
    url(r'item/create/$', AgroDealerItemCreateView.as_view(), name='item_create'),
    url(r'edit/(?P<pk>[\w]+)/$', AgroDealerUpdateView.as_view(), name='update'),
    url(r'list/$', AgroDealerListView.as_view(), name='list'),
    url(r'create/$', AgroDealerCreateView.as_view(), name='create'),
    url(r'(?P<agrodealer>[\w]+)/users/$', AgroDealerUserListView.as_view(), name='agrodealer_user'),
    url(r'(?P<agrodealer>[\w]+)/users/add/$', AgroDealerUserCreate.as_view(), name='agrodealer_user_add'),
    url(r'item/price/(?P<pk>[\w]+)/$', get_agrodealeritem_price, name='get_agrodealeritem_price')
]