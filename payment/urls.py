from django.conf.urls import url

from payment.views import *

urlpatterns = [
    
    url(r'list/$', PaymentMethodListView.as_view(), name='list')
]

