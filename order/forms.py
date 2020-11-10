from django import forms
from conf.utils import bootstrapify
from order.models import SupplyOrder, OrderItem, CustomerOrder, CustomerOrderItem, Customer


class SupplyOrderForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['supplier', 'agro_dealer', 'order_price', 'order_date']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SupplyOrderForm, self).__init__(*args, **kwargs)
        self.fields['order_price'].widget = forms.HiddenInput()
        
        if self.request.user.profile.access_level.name:
            self.fields['supplier'].widget = forms.HiddenInput()
            
        

class OrderItemForm(forms.ModelForm):
        
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
        

class CustomerOrderItemForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderItem
        fields = ['item', 'quantity']


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['customer', 'order_price']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['customer_reference', 'created_by', 'create_date', 'update_date']
        
    

bootstrapify(SupplyOrderForm)
bootstrapify(OrderItemForm)
bootstrapify(CustomerOrderItemForm)
bootstrapify(CustomerOrderForm)
bootstrapify(CustomerForm)