from django.conf.urls import url
from account.views import *

urlpatterns = [
    url(r'^transaction/$', AccountTransactionListView.as_view(), name="transaction_list"),
    url(r'^transaction/(?P<pk>[\d]+)/$', AccountTransactionDetailView.as_view(), name="transaction_detail")
]