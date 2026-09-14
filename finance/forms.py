from django import forms
from .models import Transaction

INPUT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'
SELECT_CLASSES = 'mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'type', 'status', 'due_date', 'paid_date', 'sale']
        widgets = {
            'description': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ex: Pagamento Fornecedor X / Venda #123'}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'placeholder': '0.00'}),
            'type': forms.Select(attrs={'class': SELECT_CLASSES}),
            'status': forms.Select(attrs={'class': SELECT_CLASSES}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'paid_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'sale': forms.Select(attrs={'class': SELECT_CLASSES}),
        }
