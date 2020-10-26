from django.conf.urls import url

from messaging.views import *

urlpatterns = [
        url(r'message/list/$', OutGoingMessageListView.as_view(), name='message_list'),
        url(r'message/send/$', SendMessageView.as_view(), name='message_send'),
    ]