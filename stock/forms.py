from django import forms
from .models import StockSlip, StockSlipItem
from parameters.models import Project, Warehouse


class StockSlipForm(forms.ModelForm):
    class Meta:
        model = StockSlip
        fields = ['slip_type', 'date', 'time', 'project', 'warehouse', 'description',
                  'staff', 'target_project', 'target_warehouse']
        widgets = {
            'slip_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'staff': forms.Select(attrs={'class': 'form-select'}),
            'target_project': forms.Select(attrs={'class': 'form-select'}),
            'target_warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class StockSlipItemForm(forms.ModelForm):
    class Meta:
        model = StockSlipItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


StockSlipItemFormSet = forms.inlineformset_factory(
    StockSlip, StockSlipItem, form=StockSlipItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)


class StockTransferForm(forms.Form):
    date = forms.DateField(label='Tarih', widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.TimeField(label='Saat', widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    source_project = forms.ModelChoiceField(queryset=Project.objects.filter(is_active=True),
                                            label='Kaynak Proje',
                                            widget=forms.Select(attrs={'class': 'form-select'}))
    source_warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.filter(is_active=True),
                                              label='Kaynak Depo', required=False,
                                              widget=forms.Select(attrs={'class': 'form-select'}))
    target_project = forms.ModelChoiceField(queryset=Project.objects.filter(is_active=True),
                                            label='Hedef Proje',
                                            widget=forms.Select(attrs={'class': 'form-select'}))
    target_warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.filter(is_active=True),
                                              label='Hedef Depo', required=False,
                                              widget=forms.Select(attrs={'class': 'form-select'}))
    description = forms.CharField(label='Aciklama', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))


class StockFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.filter(is_active=True),
                                     required=False, label='Proje',
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.filter(is_active=True),
                                       required=False, label='Depo',
                                       widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField(required=False, label='Baslangic',
                                 widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=False, label='Bitis',
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
