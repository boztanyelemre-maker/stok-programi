from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Kullanici Adi', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kullanici Adi'}))
    password = forms.CharField(label='Sifre', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Sifre'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'work_phone',
                  'company', 'authorized_name', 'authorized_surname',
                  'country', 'city', 'district']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'})
                   for field in fields}
        widgets['email'] = forms.EmailInput(attrs={'class': 'form-control'})


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Sifre', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Sifre Tekrar', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role',
                  'tc_kimlik', 'phone', 'title', 'company', 'projects']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'tc_kimlik': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'projects': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Sifreler eslesmiyor.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'tc_kimlik',
                  'phone', 'title', 'company', 'is_approved', 'is_active', 'projects']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'tc_kimlik': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'projects': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Eski Sifre', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Yeni Sifre', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Yeni Sifre Tekrar', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
