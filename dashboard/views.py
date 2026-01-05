from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from sales.models import Sale, SaleItem
from finance.models import Transaction
from inventory.models import Product
from .forms import CustomUserCreationForm, CustomUserChangeForm, OrganizationForm
from .models import User, Organization
import datetime

def is_admin(user):
    return user.role == 'ADMIN' or user.is_superuser

# Dashboard home view
@login_required
def index(request):
    today = timezone.now().date()
    next_7_days = today + datetime.timedelta(days=7)
    
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
    low_stock_count = Product.objects.filter(stock__lte=F('min_stock')).count()

    # New KPIs
    # Ticket Médio: (Total Vendas / Qtd Vendas) no período atual (hoje)
    sales_today_count = Sale.objects.filter(created_at__date=today).count()
    average_ticket = sales_today_amount / sales_today_count if sales_today_count > 0 else 0

    # Contas a Receber: Soma de Transaction (INCOME) pendentes nos próximos 7 dias
    receivables = Transaction.objects.filter(
        type='INCOME', 
        status='PENDING', 
        due_date__range=[today, next_7_days]
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Contas a Pagar: Soma de Transaction (EXPENSE) pendentes nos próximos 7 dias
    payables = Transaction.objects.filter(
        type='EXPENSE', 
        status='PENDING', 
        due_date__range=[today, next_7_days]
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Valor em Estoque: Soma de (Preço * Estoque) de todos os produtos
    stock_value = Product.objects.aggregate(
        total_value=Sum(F('price') * F('stock'))
    )['total_value'] or 0

    context = {
        'sales_today_amount': sales_today_amount,
        'pending_orders_count': pending_orders_count,
        'cash_flow': cash_flow,
        'low_stock_count': low_stock_count,
        'average_ticket': average_ticket,
        'receivables': receivables,
        'payables': payables,
        'stock_value': stock_value,
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def dashboard_charts_data(request):
    today = timezone.now().date()
    last_30_days = today - datetime.timedelta(days=30)
    
    # Vendas Últimos 30 Dias: Agrupamento por dia
    sales_last_30_days = Sale.objects.filter(
        created_at__date__gte=last_30_days
    ).annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total=Sum('total')
    ).order_by('day')
    
    sales_chart_labels = [item['day'].strftime('%d/%m') for item in sales_last_30_days]
    sales_chart_data = [float(item['total']) for item in sales_last_30_days]

    # Fluxo de Caixa Mensal: Receitas vs Despesas agrupadas por mês (últimos 6 meses)
    last_6_months = today - datetime.timedelta(days=180)
    
    monthly_income = Transaction.objects.filter(
        type='INCOME', 
        status='PAID',
        paid_date__gte=last_6_months
    ).annotate(
        month=TruncMonth('paid_date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')

    monthly_expenses = Transaction.objects.filter(
        type='EXPENSE', 
        status='PAID',
        paid_date__gte=last_6_months
    ).annotate(
        month=TruncMonth('paid_date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')

    # Merge income and expenses data
    months = sorted(list(set(
        [item['month'] for item in monthly_income] + 
        [item['month'] for item in monthly_expenses]
    )))
    
    cash_flow_labels = [m.strftime('%b/%Y') for m in months]
    income_data = []
    expense_data = []
    
    for m in months:
        inc = next((item['total'] for item in monthly_income if item['month'] == m), 0)
        exp = next((item['total'] for item in monthly_expenses if item['month'] == m), 0)
        income_data.append(float(inc))
        expense_data.append(float(exp))

    # Top 5 Produtos: Produtos mais vendidos (quantidade)
    top_products = SaleItem.objects.filter(
        product__isnull=False
    ).values(
        'product__name'
    ).annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:5]
    
    top_products_labels = [item['product__name'] for item in top_products]
    top_products_data = [item['total_qty'] for item in top_products]

    # Mix de Vendas: Proporção entre Produtos vs Serviços vendidos
    products_sold = SaleItem.objects.filter(product__isnull=False).aggregate(total=Sum('quantity'))['total'] or 0
    services_sold = SaleItem.objects.filter(service__isnull=False).aggregate(total=Sum('quantity'))['total'] or 0
    
    mix_labels = ['Produtos', 'Serviços']
    mix_data = [products_sold, services_sold]

    data = {
        'sales_chart': {
            'labels': sales_chart_labels,
            'data': sales_chart_data,
        },
        'cash_flow_chart': {
            'labels': cash_flow_labels,
            'income': income_data,
            'expense': expense_data,
        },
        'top_products_chart': {
            'labels': top_products_labels,
            'data': top_products_data,
        },
        'mix_chart': {
            'labels': mix_labels,
            'data': mix_data,
        }
    }
    
    return JsonResponse(data)


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
        messages.success(request, 'Usuário excluído com sucesso.')
        if request.htmx:
            users = User.objects.all()
            rows_html = render_to_string('dashboard/partials/user_list_rows.html', {'users': users}, request=request)
            messages_html = render_to_string('partials/messages.html', {}, request=request)
            final_html = rows_html + f'<tr style="display:none"><td>{messages_html}</td></tr>'
            return HttpResponse(final_html)
        return redirect('user_list')
    return render(request, 'dashboard/user_confirm_delete.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def organization_update(request):
    organization = Organization.load()
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações da organização atualizadas com sucesso.')
            return redirect('organization_update')
    else:
        form = OrganizationForm(instance=organization)
    
    return render(request, 'dashboard/organization_form.html', {'form': form})
