from django import forms
from .models import Product, Service, Supplier, Category

INPUT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'
SELECT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'document', 'contact_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Razão Social ou Nome'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'fornecedor@email.com'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '(00) 00000-0000'}),
            'document': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'CNPJ ou CPF'}),
            'contact_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome do representante/contato'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome da categoria'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'price', 'cost_price', 'stock', 'min_stock', 'unit', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome do produto'}),
            'sku': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ex: PROD-001'}),
            'category': forms.Select(attrs={'class': SELECT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'placeholder': '0.00'}),
            'cost_price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '0'}),
            'min_stock': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '0'}),
            'unit': forms.Select(attrs={'class': SELECT_CLASSES}),
            'supplier': forms.Select(attrs={'class': SELECT_CLASSES}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'estimated_duration', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome do serviço prestado'}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'placeholder': '0.00'}),
            'estimated_duration': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'HH:MM:SS (ex: 01:30:00)'}),
            'supplier': forms.Select(attrs={'class': SELECT_CLASSES}),
        }
