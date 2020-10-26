import re
import xlrd
import json
from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from conf.utils import internationalize_number
from messaging.utils import sendSMS
from messaging.models import OutgoingMessages
from messaging.forms import SendMessageForm


class OutGoingMessageListView(ListView):
    model = OutgoingMessages
    ordering = ['-sent_date']
    
    def get_context_data(self, **kwargs):
        context = super(OutGoingMessageListView, self).get_context_data(**kwargs)
        context['active'] = ['_messaging', '__sent']
        return context
    
    
    
class SendMessageView(View):

    def dispatch(self, *args, **kwargs):
        return super(SendMessageView, self).dispatch(*args, **kwargs)

    template_name = 'messaging/send_message.html'

    def get(self, request, *args, **kwargs):
        form = SendMessageForm()
        data = {
            'form': form,
            'active': ['_messaging', '__send']
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = SendMessageForm(request.POST, request.FILES)
        errors = dict()
        count = 0
        
        if form.is_valid():
            if form.cleaned_data['msisdn_file']:
                
                f = request.FILES['msisdn_file']
                path = f.temporary_file_path()
                message = form.cleaned_data['message']
                sender_id = form.cleaned_data['sender_id']
                index = int(form.cleaned_data['sheetno']) - 1
                startrow = int(form.cleaned_data['startrow']) - 1
                msisdn_col = int(form.cleaned_data['msisdn_col'])
                name_col = int(form.cleaned_data['name_col'])
                field3_col = int(form.cleaned_data['field3_col'])
                field4_col = int(form.cleaned_data['field4_col'])

                try:
                    book = xlrd.open_workbook(filename=path, logfile='/tmp/xls.log')
                    sheet = book.sheet_by_index(index)
                    numbers = []

                    for i in range(startrow, sheet.nrows):
                        message = form.cleaned_data['message']
                        network = None
                        row = sheet.row(i)
                        msisdn = None
                        msisdn_detail = None

                        try:
                            msisdn = int(row[msisdn_col].value)
                            msisdn = internationalize_number(msisdn)
                        except Exception as err:
                            print err
                            errors['error'] = "Invalid Number '%s' at ROW: %d. Please make sure the numbers are in the right column" % (
                            row[msisdn_col].value, i + 1)

                        try:
                            field1 = smart_str(row[name_col].value).strip()
                        except:
                            field1 = None
                        
                        try:
                            field3 = smart_str(row[field3_col].value).strip()
                        except:
                            field3 = None
                        try:
                            field4 = smart_str(row[field4_col].value).strip()
                        except:
                            field4 = None
                        try:
                            
                            if field1: message = message.replace("<NAME>", field1)
                            if field3: message = message.replace("<FIELD3>", str(field3))
                            if field4: message = message.replace("<FIELD4>", str(field4))
                        except UnicodeDecodeError as err:
                            print traceback.format_exc()
                            errors['error'] = "Encode Error: %s " % err

                        numbers.append({'msisdn': msisdn, 'message': message})
                except Exception as err:
                    print traceback.format_exc()
                    errors['error'] = "Error: %s " % err

            else:
                
                msisdn = form.cleaned_data['msisdn']
                message = form.cleaned_data['message']
                sender_id = form.cleaned_data['sender_id']
                
                v = 0
                numbers = []
                
                try:
                    for m in re.split("\r\n|,| ", msisdn):
                        if m:
                            try:
                                #m = unicodedata.normalize('NFKD', m).encode('ascii', 'ignore')
                                m = internationalize_number(m)
                            except ValueError as err:
                                errors['error'] = "Invalid Phone Number %s" % m
    
                            numbers.append({'msisdn': m, 'message': message})
                except Exception as err:
                    errors['error'] = "Error Occured: %s" % err

            if 'error' in errors:
                data = {
                    'form': form,
                    'errors': errors,
                    'active': 'send_sms'
                }
                return render(request, self.template_name, data)
            count_t = len(numbers)
            
            for d in numbers:
                phone_number = d['msisdn']
                msg = d['message']
                
                sendSMS(request, phone_number, message)
                # res = json.loads(send)
            return redirect('messaging:message_list')
        
        data = {
            'form': form,
            'active': ['_messaging', '__send']
        }
        return render(request, self.template_name, data)