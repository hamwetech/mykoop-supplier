from django import forms
from conf.utils import bootstrapify


class TransactionSearchForm(forms.Form):
    STATUS_CHOICES = (
        ('', '-----------'),
        ('PENDING', 'PENDING'),
        ('PROCESSING', 'PROCESSING'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
        ('FAILED', 'FAILED'),
        ('UNKNOWN', 'UNKNOWN'),
    )
    search = forms.CharField(max_length=26, required=False)
    start_date = forms.CharField(max_length=26, required=False)
    end_date = forms.CharField(max_length=26, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)


bootstrapify(TransactionSearchForm)
