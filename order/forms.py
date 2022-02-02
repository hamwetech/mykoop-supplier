from django import forms
from conf.utils import bootstrapify, internationalize_number
from supplier.models import Supplier, Item
from order.models import SupplyOrder, OrderItem, CustomerOrder, CustomerOrderItem, Customer


class SupplyOrderForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['customer', 'order_price', 'order_price', 'payment_mode', 'order_date']

        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SupplyOrderForm, self).__init__(*args, **kwargs)
        # self.fields['order_price'].widget = forms.HiddenInput()
        self.fields['order_date'].widget.attrs["data-uk-datepicker"] = "{format:'YYYY-MM-DD'}"
       
        # if not self.request.user.is_superuser:
        #     if self.request.user.profile.access_level.name == 'SUPPLIER':
        #         self.fields['supplier'].widget = forms.HiddenInput()
            

class OrderItemForm(forms.ModelForm):
        
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        # self.fields['item'].queryset = Item.objects.none()
        

class CustomerOrderItemForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderItem
        fields = ['item', 'quantity']


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['customer', 'order_price']
        
    def __init__(self, *args, **kwargs):
        super(CustomerOrderForm, self).__init__(*args, **kwargs)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['customer_reference', 'created_by', 'create_date', 'update_date']


class MakePaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=12)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            phone_number = internationalize_number(phone_number)
        except Exception as e:
            raise forms.ValidationError('Invalid Number Provided')
        self.cleaned_data['phone_number'] = phone_number
        return self.cleaned_data


class OrderSearchForm(forms.Form):
    customer = forms.ChoiceField()
    status = forms.ChoiceField()


bootstrapify(MakePaymentForm)
bootstrapify(SupplyOrderForm)
bootstrapify(OrderItemForm)
bootstrapify(CustomerOrderItemForm)
bootstrapify(CustomerOrderForm)
bootstrapify(CustomerForm)