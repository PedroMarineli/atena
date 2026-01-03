from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db import transaction, models
from django.utils import timezone
from django.contrib import messages
from .models import Sale, SaleItem, Customer
from .forms import SaleForm, SaleItemForm, CustomerForm
from finance.models import Transaction
from dashboard.views import is_admin
# from inventory.models import Item

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                customers = Customer.objects.all()
                return render(request, 'sales/partials/customer_list_rows.html', {'customers': customers})
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    context = {'form': form, 'submit_url': reverse('customer_create'), 'modal_title': 'Novo Cliente'}
    if request.htmx:
        return render(request, 'sales/partials/customer_form.html', context)
    return render(request, 'sales/customer_form.html', context)

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if request.htmx:
                customers = Customer.objects.all()
                return render(request, 'sales/partials/customer_list_rows.html', {'customers': customers})
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    context = {'form': form, 'submit_url': reverse('customer_update', args=[pk]), 'modal_title': 'Editar Cliente'}
    if request.htmx:
        return render(request, 'sales/partials/customer_form.html', context)
    return render(request, 'sales/customer_form.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE", "POST"])
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    try:
        customer.delete()
        messages.success(request, 'Cliente excluído com sucesso.')
    except models.ProtectedError:
        messages.error(request, 'Não é possível excluir este cliente pois existem vendas associadas a ele.')
    
    if request.htmx:
        customers = Customer.objects.all()
        rows_html = render_to_string('sales/partials/customer_list_rows.html', {'customers': customers}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        return HttpResponse(rows_html + messages_html)
    return redirect('customer_list')

@login_required
def sale_list(request):
    sales = Sale.objects.select_related('customer', 'seller').all()
    return render(request, 'sales/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.seller = request.user
            sale.save()
            if request.htmx:
                sales = Sale.objects.all()
                return render(request, 'sales/partials/sale_list_rows.html', {'sales': sales})
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    
    if request.htmx:
        return render(request, 'sales/partials/sale_form.html', {'form': form})
    return render(request, 'sales/sale_form.html', {'form': form})

@login_required
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            if request.htmx:
                sales = Sale.objects.all()
                return render(request, 'sales/partials/sale_list_rows.html', {'sales': sales})
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    
    if request.htmx:
        return render(request, 'sales/partials/sale_form.html', {'form': form, 'sale': sale})
    return render(request, 'sales/sale_form.html', {'form': form, 'sale': sale})
    
@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE", "POST"])
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    if sale.status == 'COMPLETED':
        with transaction.atomic():
            # Restore stock
            for item in sale.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
            
            # Delete associated transactions
            sale.transactions.all().delete()

    sale.delete()
    messages.success(request, 'Venda excluída com sucesso.')
    if request.htmx:
        sales = Sale.objects.all()
        rows_html = render_to_string('sales/partials/sale_list_rows.html', {'sales': sales}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        return HttpResponse(rows_html + messages_html)
    return redirect('sale_list')

@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    form = SaleItemForm()

    return render(request, 'sales/sale_detail.html', {'sale': sale, 'items': items, 'form': form})

@login_required
def sale_add_item(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if sale.status == 'COMPLETED':
        messages.error(request, 'Não é possível adicionar itens a uma venda finalizada.')
        if request.htmx:
            rows_html = render_to_string('sales/partials/sale_items.html', {'sale': sale}, request=request)
            messages_html = render_to_string('partials/messages.html', {}, request=request)
            return HttpResponse(rows_html + messages_html)
        return redirect('sale_detail', pk=pk)

    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            sale_item = form.save(commit=False)
            sale_item.sale = sale
            
            # Check stock availability
            if sale_item.product:
                if sale_item.product.stock < sale_item.quantity:
                    messages.error(request, f'Estoque insuficiente para {sale_item.product.name}. Disponível: {sale_item.product.stock}')
                    if request.htmx:
                        rows_html = render_to_string('sales/partials/sale_items.html', {'sale': sale}, request=request)
                        messages_html = render_to_string('partials/messages.html', {}, request=request)
                        return HttpResponse(rows_html + messages_html)
                    return redirect('sale_detail', pk=pk)

            if sale_item.product:
                sale_item.price = sale_item.product.price
            elif sale_item.service:
                sale_item.price = sale_item.service.price
            else:
                sale_item.price = 0
            
            sale_item.save()
            # Update sale total
            sale.total = sum(item.quantity * item.price for item in sale.items.all())
            sale.save()
            
            messages.success(request, 'Item adicionado com sucesso.')
            if request.htmx:
                rows_html = render_to_string('sales/partials/sale_items.html', {'sale': sale}, request=request)
                messages_html = render_to_string('partials/messages.html', {}, request=request)
                return HttpResponse(rows_html + messages_html)
    return redirect('sale_detail', pk=pk)
    return redirect('sale_detail', pk=pk)

@require_http_methods(["DELETE", "POST"])
def sale_remove_item(request, pk, item_pk):
    sale = get_object_or_404(Sale, pk=pk)

    if sale.status == 'COMPLETED':
        messages.error(request, 'Não é possível remover itens de uma venda finalizada.')
        if request.htmx:
            rows_html = render_to_string('sales/partials/sale_items.html', {'sale': sale}, request=request)
            messages_html = render_to_string('partials/messages.html', {}, request=request)
            return HttpResponse(rows_html + messages_html)
        return redirect('sale_detail', pk=pk)

    item = get_object_or_404(SaleItem, pk=item_pk, sale=sale)
    item.delete()
    
    # Update sale total
    sale.total = sum(item.quantity * item.price for item in sale.items.all())
    sale.save()
    
    messages.success(request, 'Item removido com sucesso.')
    if request.htmx:
        rows_html = render_to_string('sales/partials/sale_items.html', {'sale': sale}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        return HttpResponse(rows_html + messages_html)
    return redirect('sale_detail', pk=pk)

@login_required
@require_http_methods(["POST"])
def sale_finalize(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    if sale.status == 'COMPLETED':
        messages.warning(request, 'Esta venda já foi finalizada.')
        return redirect('sale_detail', pk=pk)
        
    if not sale.items.exists():
        messages.error(request, 'Não é possível finalizar uma venda sem itens.')
        return redirect('sale_detail', pk=pk)

    try:
        with transaction.atomic():
            # 1. Deduct stock from Inventory (for Products)
            for item in sale.items.all():
                if item.product:
                    # Refresh product from db to ensure stock is up to date
                    item.product.refresh_from_db()
                    if item.product.stock < item.quantity:
                        raise ValueError(f'Estoque insuficiente para o produto {item.product.name}. Estoque atual: {item.product.stock}')
                    item.product.stock -= item.quantity
                    item.product.save()
            
            # 2. Generate a "Receivable" (Transaction type=INCOME) in Finance
            Transaction.objects.create(
                description=f"Venda #{sale.id} - {sale.customer.name}",
                amount=sale.total,
                type='INCOME',
                status='PAID',
                due_date=timezone.now().date(),
                paid_date=timezone.now().date(),
                sale=sale
            )
            
            # 3. Update sale status
            sale.status = 'COMPLETED'
            sale.save()
            
            messages.success(request, 'Venda finalizada com sucesso!')
            
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f'Erro ao finalizar venda: {str(e)}')
        
    return redirect('sale_detail', pk=pk)
