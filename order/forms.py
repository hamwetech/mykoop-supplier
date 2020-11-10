from django import forms
from conf.utils import bootstrapify
from supplier.models import Supplier, Item
from order.models import SupplyOrder, OrderItem, CustomerOrder, CustomerOrderItem, Customer


class SupplyOrderForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['supplier', 'agro_dealer', 'order_price', 'order_date']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SupplyOrderForm, self).__init__(*args, **kwargs)
        self.fields['order_price'].widget = forms.HiddenInput()
        print(self.request.user.agro_dealer_user.agrodealer.id)
        if not self.request.user.is_superuser:
            if self.request.user.profile.access_level.name == 'SUPPLIER':
                self.fields['supplier'].widget = forms.HiddenInput()
            if self.request.user.profile.access_level.name == 'AGRODEALER':
                self.fields['agro_dealer'].widget = forms.HiddenInput()
                self.fields['agro_dealer'].initial = self.request.user.agro_dealer_user.agrodealer
            

class OrderItemForm(forms.ModelForm):
        
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.none()
        

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