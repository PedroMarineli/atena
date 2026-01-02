from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                transactions = Transaction.objects.all()
                return render(request, 'finance/partials/transaction_list_rows.html', {'transactions': transactions})
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    
    if request.htmx:
        return render(request, 'finance/partials/transaction_form.html', {'form': form})
    return render(request, 'finance/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            if request.htmx:
                transactions = Transaction.objects.all()
                return render(request, 'finance/partials/transaction_list_rows.html', {'transactions': transactions})
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    if request.htmx:
        return render(request, 'finance/partials/transaction_form.html', {'form': form, 'transaction': transaction})
    return render(request, 'finance/transaction_form.html', {'form': form, 'transaction': transaction})

@login_required
@require_http_methods(["DELETE", "POST"])
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    if request.htmx:
        transactions = Transaction.objects.all()
        return render(request, 'finance/partials/transaction_list_rows.html', {'transactions': transactions})
    return redirect('transaction_list')
