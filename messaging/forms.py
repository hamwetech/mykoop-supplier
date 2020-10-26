from django import forms
from conf.utils import bootstrapify


class SendMessageForm(forms.Form):
    sheetno_choices = [['1', 'Sheet 1'], ['2', 'Sheet 2'], ['3', 'Sheet 3'], ['4', 'Sheet 4']]
    startrow_choices = [['1', 'Row 1'], ['2', 'Row 2'], ['3', 'Row 3'], ['4', 'Row 4'], ['5', 'Row 5']]

    choices = list()
    for i in range(65, 91):
        choices.append([i - 65, chr(i)])

    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'rows':'4', 'maxlength': '480'}), help_text="To add a name to the message, use #NAME# where you want the name to go in the message. This only works when using an excel file or if your saved contacts have names. To add other fields use #FIELD3# or #FIELD4# where you want the filed to go in the message. This works with Excel ONLY")
    sender_id = forms.CharField(max_length=15, initial='6565',  widget=forms.TextInput(attrs={'readonly':'readonly'}))
    msisdn = forms.CharField(label='Phone Number(s)', required=False, widget=forms.Textarea(attrs={'rows': '4'}))
    
    msisdn_file = forms.FileField(required=False)
    sheetno = forms.ChoiceField(required=False, label='Sheet Number', choices=sheetno_choices,
                          widget=forms.Select(attrs={'class': ' form-control '}), help_text='')
    startrow = forms.ChoiceField(required=False, label='Record Start Row', choices=startrow_choices,
                           widget=forms.Select(attrs={'class': ' form-control '}), help_text='')
    msisdn_col = forms.ChoiceField(required=False, initial=0, choices=choices,
                             widget=forms.Select(attrs={'class': ' form-control '}))
    name_col = forms.ChoiceField(required=False, initial=1, choices=choices,
                             widget=forms.Select(attrs={'class': ' form-control '}))
    field3_col = forms.ChoiceField(required=False, initial=3, choices=choices,
                             widget=forms.Select(attrs={'class': ' form-control '}))
    field4_col = forms.ChoiceField(required=False, initial=4, choices=choices,
                             widget=forms.Select(attrs={'class': ' form-control '}))

    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)

        

    def clean(self):
        cleaned_data = super(SendMessageForm, self).clean()
        file = cleaned_data.get('msisdn_file')
        msisdn = cleaned_data.get('msisdn')
       
        if not file and not msisdn:
            raise forms.ValidationError(
                'Please Provide Phone Numbers by file or by typing in the Msisdn box or Select a list from the Phonebook')

bootstrapify(SendMessageForm)