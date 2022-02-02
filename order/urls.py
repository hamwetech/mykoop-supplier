from django.conf.urls import url
from order.views import SupplyOrderListView, SupplyOrderCreateView, SupplyOrderDetailView, update_status, CustomerOrderListView,\
CustomerOrderCreateView, CustomerOrderDetailView, update_customer_order_status, CustomerCreateView, CustomerListView, SupplyOrderDeleteView,\
load_supplier_items, update_item_status, OrderPaymentView, SupplierItemOrderList


urlpatterns = [
    # url(r'edit/(?P<pk>[\w]+)/$', AgroDealerUpdateView.as_view(), name='update'),
    
    url(r'account/customer/create/$', CustomerCreateView.as_view(), name='customer_create'),
    url(r'account/customer/list/$', CustomerListView.as_view(), name='customer_list'),
    
    url(r'customer/create/$', CustomerOrderCreateView.as_view(), name='order_create'),
    url(r'customer/list/$', CustomerOrderListView.as_view(), name='order_list'),
    url(r'customer/detail/(?P<pk>[\d]+)/$', CustomerOrderDetailView.as_view(), name='order_detail'),
    url(r'customer/update/status/', update_customer_order_status, name='order_status'),
    url(r'item/list/$', SupplierItemOrderList.as_view(), name='item_list'),

    url(r'create/$', SupplyOrderCreateView.as_view(), name='create'),
    url(r'list/$', SupplyOrderListView.as_view(), name='list'),
    url(r'detail/(?P<pk>[\d]+)/$', SupplyOrderDetailView.as_view(), name='detail'),
    url(r'delete/(?P<pk>[\d]+)/$', SupplyOrderDeleteView.as_view(), name='delete'),
    url(r'payment/(?P<pk>[\d]+)/$', OrderPaymentView.as_view(), name='order_payment'),

    url(r'update/status/', update_status, name='order_success'),
    url(r'item/status/', update_item_status, name='order_item_status'),
    url(r'update/order/status/', update_customer_order_status, name='order_status'),
    url(r'supplier/item/json/', load_supplier_items, name='supplier_item'),
    
]