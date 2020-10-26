# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import datetime
import string
import random
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from userprofile.models import Profile
from conf.models import District, County, SubCounty, Village
from supplier.models import Supplier, Item, OrderItem
from apiv1.serializers import *

from django.shortcuts import render


class SupplierListView(APIView):
    pass


class ItemsListView(APIView):
    def post(self, request, member=None, format=None):
        suppliers = Supplier.objects.all()
        payload = dict()
        ar = []
        for s in suppliers:
            payload.update({'supplier': s.name})
            items = Item.objects.filter(supplier=s)

            for i in items:
                ar.append({'item':i.name, 'price':i.price})
            payload.update(ar)
        return Response(payload)
