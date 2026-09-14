from django import forms
from .models import Sale, SaleItem, Customer

INPUT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'
SELECT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'document', 'address', 'city', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome completo ou Razão Social'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'cliente@email.com'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '(00) 00000-0000'}),
            'document': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'CPF ou CNPJ'}),
            'address': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Rua, número, complemento, bairro'}),
            'city': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Cidade'}),
            'state': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'UF'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': SELECT_CLASSES}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'service', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': SELECT_CLASSES}),
            'service': forms.Select(attrs={'class': SELECT_CLASSES}),
            'quantity': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': '1', 'value': '1'}),
        }
