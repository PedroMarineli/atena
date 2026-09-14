from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Organization

INPUT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'
SELECT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'
FILE_CLASSES = 'mt-1 block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition'
CHECKBOX_CLASSES = 'h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500/30'

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'logo', 'cnpj', 'phone', 'email', 'address', 'pix_key', 'receipt_footer_text')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'logo': forms.FileInput(attrs={'class': FILE_CLASSES}),
            'cnpj': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '00.000.000/0000-00'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'contato@empresa.com'}),
            'address': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3}),
            'pix_key': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Chave CNPJ, e-mail, telefone ou aleatória'}),
            'receipt_footer_text': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')
        widgets = {
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'usuario@empresa.com'}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'role': forms.Select(attrs={'class': SELECT_CLASSES}),
        }

class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove password from the form

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'is_active')
        widgets = {
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'role': forms.Select(attrs={'class': SELECT_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
        }
