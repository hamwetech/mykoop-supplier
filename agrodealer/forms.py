from django import forms
from models import AgroDealer, AgroDealerCategory, AgroDealerItem
from conf.utils import bootstrapify


class AgroDealerForm(forms.ModelForm):
    class Meta:
        model = AgroDealer
        exclude = ['create_date', 'update_date']
        

class AgroDealerItemForm(forms.ModelForm):
    class Meta:
        model = AgroDealerItem
        exclude = ['create_date', 'update_date']
        

class AgroDealerCategoryForm(forms.ModelForm):
    class Meta:
        model = AgroDealerCategory
        exclude = ['create_date', 'update_date']


bootstrapify(AgroDealerItemForm)
bootstrapify(AgroDealerCategoryForm)
bootstrapify(AgroDealerForm)
        
