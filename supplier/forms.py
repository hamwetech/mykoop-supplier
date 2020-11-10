from django import forms
from conf.utils import bootstrapify
from supplier.models import Supplier, SupplierUser, Item, Category


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['create_date', 'update_date']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['create_date', 'update_date']
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['create_date', 'update_date']


bootstrapify(ItemForm)
bootstrapify(SupplierForm)