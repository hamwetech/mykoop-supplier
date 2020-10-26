from django.conf.urls import url

from conf.views import *

urlpatterns = [
     url(r'sms/template/$', MessageTemplatesView.as_view(), name='sms_template'),
     url(r'district/list/$', DistrictListView.as_view(), name='district_list'),
     url(r'district/create/$', DistrictCreateView.as_view(), name='district_create'),
     url(r'district/(?P<pk>[\w]+)/$', DistrictUpdateView.as_view(), name='district_edit'),
     url(r'county/create/$', CountyCreateView.as_view(), name='county_create'),
     url(r'county/list/$', CountyListView.as_view(), name='county_list'),
     url(r'county/(?P<pk>[\w]+)/$', CountyUpdateView.as_view(), name='county_edit'),

     url(r'sc/create/$', SubCountyCreateView.as_view(), name='subcounty_create'),
     url(r'sc/list/$', SubCountyListView.as_view(), name='subcounty_list'),
     url(r'sc/(?P<pk>[\w]+)/$', SubCountyUpdateView.as_view(), name='subcounty_edit'),
     url(r'village/create/$', VillageCreateView.as_view(), name='village_create'),
     url(r'village/list/$', VillageListView.as_view(), name='village_list'),
     url(r'village/(?P<pk>[\w]+)/$', VillageUpdateView.as_view(), name='village_edit'),
     url(r'payment/create/$', PaymentModeCreateView.as_view(), name='payment_create'),
     url(r'payment/list/$', PaymentModeListView.as_view(), name='payment_list'),
     url(r'payment/(?P<pk>[\w]+)/$', PaymentModeUpdateView.as_view(), name='payment_edit'),
     
     url(r'upload/location/$', LocationUploadView.as_view(), name='location_upload'),
    ]
