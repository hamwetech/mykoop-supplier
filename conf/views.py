# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import xlrd

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q, Count, Sum
from django.utils.encoding import smart_str
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from conf.utils import log_debug, log_error
from conf.models import District, County, SubCounty, Parish, Village, PaymentMethod, MessageTemplates
from conf.forms import DistrictForm, CountyForm, SubCountyForm, VillageForm, PaymentMethodForm, UploadLocation,\
MessageTemplatesForm

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_config']
        context['title'] = 'System Settings'
        context.update(self.extra_context)
        return context


class DistrictListView(ExtraContext, ListView):
    model = District
    extra_context = {'active': ['_config', '__district']}
    

class DistrictCreateView(ExtraContext, CreateView):
    model = District
    form_class = DistrictForm
    extra_context = {'active': ['_config', '__district']}
    success_url = reverse_lazy('conf:district_list')


class DistrictUpdateView(ExtraContext, UpdateView):
    model = District
    form_class = DistrictForm
    extra_context = {'active': ['_config', '__district']}
    success_url = reverse_lazy('conf:district_list')


class CountyListView(ExtraContext, ListView):
    model = County
    extra_context = {'active': ['_config', '__county']}


class CountyCreateView(ExtraContext, CreateView):
    model = County
    form_class = CountyForm
    extra_context = {'active': ['_config', '__county']}
    success_url = reverse_lazy('conf:county_list')


class CountyUpdateView(ExtraContext, UpdateView):
    model = County
    form_class = CountyForm
    extra_context = {'active': ['_config', '__county']}
    success_url = reverse_lazy('conf:county_list')


class SubCountyListView(ExtraContext, ListView):
    model = SubCounty
    extra_context = {'active': ['_config', '__sub_county']}
    
    
class SubCountyCreateView(ExtraContext, CreateView):
    model = SubCounty
    form_class = SubCountyForm
    extra_context = {'active': ['_config', '__sub_county']}
    success_url = reverse_lazy('conf:subcounty_list')


class SubCountyUpdateView(ExtraContext, UpdateView):
    model = SubCounty
    form_class = SubCountyForm
    extra_context = {'active': ['_config', '__sub_county']}
    success_url = reverse_lazy('conf:subcounty_list')
    

class VillageListView(ExtraContext, ListView):
    model = Parish
    template_name = "conf/village_list.html"
    order_by = '-name'
    extra_context = {'active': ['_config', '__village']}
    # paginate_by = 10
        
    def get_queryset(self):
        queryset = None
        village = self.request.GET.get('village')
        subcounty = self.request.GET.get('subcounty')
        county = self.request.GET.get('county')
        district = self.request.GET.get('district')
        queryset = Parish.objects.all()
        if village:
            queryset = queryset.filter(name=query)
        if subcounty:
            queryset = queryset.filter(name__sub_county__name=subcounty)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(VillageListView, self).get_context_data(**kwargs)
        return context
    

class VillageCreateView(ExtraContext, CreateView):
    model = Parish
    template_name = "conf/village_form.html"
    form_class = VillageForm
    extra_context = {'active': ['_config', '__village']}
    success_url = reverse_lazy('conf:village_list')

class VillageUpdateView(ExtraContext, UpdateView):
    model = Parish
    template_name = "conf/village_form.html"
    form_class = VillageForm
    extra_context = {'active': ['_config', '__village']}
    success_url = reverse_lazy('conf:village_list')
    

class PaymentModeListView(ExtraContext, ListView):
    model = PaymentMethod
    extra_context = {'active': ['_config', '__sub_county']}
    

class PaymentModeCreateView(ExtraContext, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    extra_context = {'active': ['_config', '__payment_method']}
    success_url = reverse_lazy('conf:payment_list')

class PaymentModeUpdateView(ExtraContext, UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    extra_context = {'active': ['_config', '__payment_method']}
    success_url = reverse_lazy('conf:payment_list')
    
class LocationUploadView(ExtraContext, View):

    # @method_decorator(is_authorized(all=['system.add_location']))
    # def dispatch(self, *args, **kwargs):
    #     return super(LocationUploadView, self).dispatch(*args, **kwargs)

    template_name = 'conf/location_upload.html'
    
    def dispatch(self, request, *args, **kwargs):
        #messages.success(self.request, "Book viewed!")
        extra_context = {'active': ['_config', '__village']}
        return super(LocationUploadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UploadLocation
        return render(request, self.template_name, {'active': 'setting', 'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form = UploadLocation(request.POST, request.FILES)
        
        if form.is_valid():
            f = request.FILES['uploadfile']
            
            path = f.temporary_file_path()
            index = int(form.cleaned_data['sheet'])-1
            startrow = int(form.cleaned_data['row'])-1
            district_col = int(form.cleaned_data['district_col'])
            county_col = int(form.cleaned_data['county_col'])
            sub_county_col = int(form.cleaned_data['sub_county_col'])
            parish_col = int(form.cleaned_data['parish_col'])
            clear_data = form.cleaned_data['clear_data']            
    
            book = xlrd.open_workbook(filename=path, logfile='/tmp/xls.log')
            sheet = book.sheet_by_index(index)
            rownum = 0
            data = dict()
            locations = []
            for i in range(startrow, sheet.nrows):
                try:
                    row = sheet.row(i)
                    rownum = i+1
                    district = smart_str(row[district_col].value).strip()
        
                    if not re.search('^[A-Z\s\(\)\-\.]+$', district, re.IGNORECASE):
                        if (i+1) == sheet.nrows: break
                        data['errors'] = '"%s" is not a valid District (row %d)' % \
                        (district, i+1)
                        return render(request, self.template_name, {'active': 'system', 'form':form, 'error': data})
        
                    county = smart_str(row[county_col].value).strip()
        
                    if not re.search('^[A-Z\s\(\)\-\.]+$', county, re.IGNORECASE):
                        data['errors'] = '"%s" is not a valid County (row %d)' % \
                        (county, i+1)
                        return render(request, self.template_name, {'active': 'system', 'form':form, 'error': data})
                    
                    sub_county = smart_str(row[sub_county_col].value).strip()
        
                    if not re.search('^[A-Z\s\(\)\-\.]+$', sub_county, re.IGNORECASE):
                        data['errors'] = '"%s" is not a valid Sub County (row %d)' % \
                        (sub_county, i+1)
                        return render(request, self.template_name, {'active': 'system', 'form':form, 'error': data})
                    
                    parish = smart_str(row[parish_col].value).strip()
        
                    if not re.search('^[A-Z\s\(\)\-\.]+$', parish, re.IGNORECASE):
                        data['errors'] = '"%s" is not a valid Parish (row %d)' % \
                        (parish, i+1)
                        return render(request, self.template_name, {'active': 'system', 'form':form, 'error': data})
                    
                    q = {'district': district, 'county': county,'sub_county':sub_county, 'parish': parish}
                    locations.append(q)
             
                except Exception as err:
                    log_error()
                    return render(request, self.template_name, {'active': 'setting', 'form':form, 'error': err})
            try:
                with transaction.atomic():
                    if clear_data:
                        District.objects.all().delete()
                        County.objects.all().delete()
                        SubCounty.objects.all().delete()
                    dcount = 0
                    ccount = 0
                    sccount = 0
                    pcount = 0
                    for d in locations:
                        district = d['district'].title()
                        county = d['county'].title()
                        sub_county = d['sub_county'].title()
                        parish = d['parish'].title()
                        
                        di = None
                        ci = None
                        
                        dq = District.objects.filter(name__iexact = district)
                        if dq.exists():
                            di = dq[0]
                        else:
                            di = District(name = district)
                            di.save()
                            dcount += 1
                            
                        
                        cq = County.objects.filter(district=di, name__iexact = county)
                        if not cq.exists():
                            ci = County(district=di, name=county)
                            ci.save()
                            ccount += 1
                        else:
                            ci = cq[0]
                        scq = SubCounty.objects.filter(county=ci, name__iexact=sub_county)
                        if not scq.exists():
                            sci = SubCounty(county=ci, name=sub_county)
                            sci.save()
                            sccount += 1
                        else:
                            sci = scq[0]
                        
                        parishq = Parish.objects.filter(sub_county=sci, name__iexact=parish)
                        
                        if not parishq.exists():
                            p = Parish(sub_county=sci, name=parish)
                            p.save()
                            pcount += 1
                    # messages.success(self.request, "%s District added, %s County's added, %s Sub-County's added" % (dcount, ccount, sccount))
                    return redirect('conf:district_list')
            except Exception as e:
                log_error()
                   
        return render(request, self.template_name, {'active': 'settings', 'form':form})


class MessageTemplatesView(View):
    template_name = 'conf/messagetemplates_form.html'
    
    def get(self, request, *args, **kwargs):
        instance = None
        q = MessageTemplates.objects.filter(pk=1)
        if q.exists():
            instance = q[0]
        form = MessageTemplatesForm(instance=instance)
        return render(request, self.template_name, {'active': ['_config', '__messageT'], 'form': form})
    
    
    def post(self, request, *args, **kwargs):
        instance = None
        q = MessageTemplates.objects.filter(pk=1)
        if q.exists():
            instance = q[0]
        form = MessageTemplatesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'active': ['_config', '__messageT'], 'form': form})
    

class Handle404(TemplateView):
    template_name = "conf/http404.html"
    
class Handle403(TemplateView):
    template_name = "conf/http403.html"
