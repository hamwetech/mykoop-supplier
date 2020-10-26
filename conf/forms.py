from django import forms

from conf.models import District, County, SubCounty, Village, Parish, PaymentMethod, MessageTemplates
from conf.utils import bootstrapify

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name']


class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = ['district', 'name']


class SubCountyForm(forms.ModelForm):
    class Meta:
        model = SubCounty
        fields = ['county', 'name']
        
class VillageForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['name', 'sub_county']
        
        
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['method']
        
        
class UploadLocation(forms.Form):
    
    sheetChoice = (
        ('1','sheet1'),
        ('2','sheet2'),
        ('3','sheet3'),
        ('4','sheet4'),
        ('5','sheet5'),
    )
    
    rowchoices = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5')
        )
    
    choices = list()
    for i in range(65, 91):
        choices.append([i-65, chr(i)])

    
    uploadfile = forms.FileField(label="Excel File", max_length=100)
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class':'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class':'form-control'}))
    district_col = forms.ChoiceField(label='District Column', initial=0, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the District')
    county_col = forms.ChoiceField(label='County Column', initial=1, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the County')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=2, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Sub County')
    parish_col = forms.ChoiceField(label='Parish Column', initial=3, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text="The column contains the Parish")
    clear_data = forms.BooleanField(initial=False, required=False, help_text="Select to Clear the Saved Data")


class MessageTemplatesForm(forms.ModelForm):
    class Meta:
        model = MessageTemplates
        exclude = ['create_date', 'update_date']
    
bootstrapify(DistrictForm)
bootstrapify(SubCountyForm)
bootstrapify(VillageForm)
bootstrapify(PaymentMethodForm)
bootstrapify(UploadLocation)
bootstrapify(MessageTemplatesForm)
bootstrapify(CountyForm)
