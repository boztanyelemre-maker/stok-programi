from django import forms
from .models import Product, MainCategory, SubCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'stock_code', 'name', 'unit', 'price', 'main_category',
                  'sub_category', 'brand', 'model', 'description', 'critical_stock_level', 'image']
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'main_category': forms.Select(attrs={'class': 'form-select'}),
            'sub_category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'critical_stock_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['main_category', 'name']
        widgets = {
            'main_category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
