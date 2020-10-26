from django import forms
from conf.utils import bootstrapify
from supplier.models import Supplier, SupplierUser, Item, OrderItem


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['create_date', 'update_date']


bootstrapify(ItemForm)
bootstrapify(SupplierForm)