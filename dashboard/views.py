from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from sales.models import Sale
from finance.models import Transaction
from inventory.models import Product
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

def is_admin(user):
    return user.role == 'ADMIN' or user.is_superuser

# Dashboard home view
@login_required
def index(request):
    today = timezone.now().date()
    
    # Sales Today
    sales_today_amount = Sale.objects.filter(
        created_at__date=today
    ).aggregate(Sum('total'))['total__sum'] or 0
    
    # Pending Orders
    pending_orders_count = Sale.objects.filter(status='PENDING').count()
    
    # Cash Flow (Income - Expenses) - Simplified
    income = Transaction.objects.filter(type='INCOME', status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Transaction.objects.filter(type='EXPENSE', status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    cash_flow = income - expenses

    # Low Stock Products
    low_stock_count = Product.objects.filter(stock__lte=5).count()

    context = {
        'sales_today_amount': sales_today_amount,
        'pending_orders_count': pending_orders_count,
        'cash_flow': cash_flow,
        'low_stock_count': low_stock_count,
    }
    
    return render(request, 'dashboard/index.html', context)

# User CRUD
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                users = User.objects.all()
                return render(request, 'dashboard/partials/user_list_rows.html', {'users': users})
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form, 'submit_url': reverse('user_create'), 'modal_title': 'Novo Usuário'}
    if request.htmx:
        return render(request, 'dashboard/partials/user_form.html', context)
    return render(request, 'dashboard/user_form.html', context)

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if request.htmx:
                users = User.objects.all()
                return render(request, 'dashboard/partials/user_list_rows.html', {'users': users})
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {'form': form, 'submit_url': reverse('user_update', args=[pk]), 'modal_title': 'Editar Usuário'}
    if request.htmx:
        return render(request, 'dashboard/partials/user_form.html', context)
    return render(request, 'dashboard/user_form.html', context)

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method in ['POST', 'DELETE']:
        user.delete()
        if request.htmx:
            users = User.objects.all()
            return render(request, 'dashboard/partials/user_list_rows.html', {'users': users})
        return redirect('user_list')
    return render(request, 'dashboard/user_confirm_delete.html', {'user': user})
