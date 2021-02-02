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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(self.user)
        super(AgroDealerItemForm, self).__init__(*args, **kwargs)
        if self.user.profile.access_level.name == "AGRODEALER":
            self.fields['agrodealer'].initial = self.user.agro_dealer_user.agrodealer.id
            self.fields['agrodealer'].widget = forms.HiddenInput()


class AgroDealerCategoryForm(forms.ModelForm):
    class Meta:
        model = AgroDealerCategory
        exclude = ['create_date', 'update_date']


bootstrapify(AgroDealerItemForm)
bootstrapify(AgroDealerCategoryForm)
bootstrapify(AgroDealerForm)
        
