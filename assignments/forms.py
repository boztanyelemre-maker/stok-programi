from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assigned_to_name', 'assigned_to_user', 'tc_kimlik', 'title',
                  'project', 'product', 'asset', 'quantity',
                  'assignment_date', 'status', 'description']
        widgets = {
            'assigned_to_name': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to_user': forms.Select(attrs={'class': 'form-select'}),
            'tc_kimlik': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'assignment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
