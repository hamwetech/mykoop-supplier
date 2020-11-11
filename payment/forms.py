import xlrd
from django import forms
from os.path import splitext
from conf.utils import bootstrapify


class PaymentFilterForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)
    start_date = forms.CharField(max_length=160, required=False, widget=forms.TextInput(attrs={"data-uk-datepicker":"{format:'YYYY-MM-DD'}"}))
    end_date = forms.CharField(max_length=160, required=False, widget=forms.TextInput(attrs={"data-uk-datepicker":"{format:'YYYY-MM-DD'}"}))
    
    payment_method = forms.ChoiceField(widget=forms.Select(), required=False, choices=(('', '------------'), ('CASH', 'CASH'), ('BANK', 'BANK'), ('MOBILE MONEY', 'MOBILE MONEY')))
    status = forms.ChoiceField(widget=forms.Select(), required=False, choices=(('', '------------'), ('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')))
  
    def __init__(self, *args, **kwargs):
        super(PaymentFilterForm, self).__init__(*args, **kwargs)
       

bootstrapify(PaymentFilterForm)
        
    
