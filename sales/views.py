from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Sale, SaleItem, Customer
from .forms import SaleForm, SaleItemForm, CustomerForm
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
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'sales/customer_confirm_delete.html', {'customer': customer})

@login_required
def sale_list(request):
    sales = Sale.objects.all()
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
@require_http_methods(["DELETE", "POST"])
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    if request.htmx:
        sales = Sale.objects.all()
        return render(request, 'sales/partials/sale_list_rows.html', {'sales': sales})
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
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            sale_item = form.save(commit=False)
            sale_item.sale = sale
            sale_item.price = sale_item.item.price # Set price from item
            sale_item.save()
            # Update sale total
            sale.total = sum(item.quantity * item.price for item in sale.items.all())
            sale.save()
            
            if request.htmx:
                return render(request, 'sales/partials/sale_items.html', {'sale': sale})
@login_required
def sale_add_item(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            sale_item = form.save(commit=False)
            sale_item.sale = sale
            # sale_item.price = sale_item.item.price # Set price from item
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
            
            if request.htmx:
                return render(request, 'sales/partials/sale_items.html', {'sale': sale})
    return redirect('sale_detail', pk=pk)

@require_http_methods(["DELETE", "POST"])
def sale_remove_item(request, pk, item_pk):
    sale = get_object_or_404(Sale, pk=pk)
    item = get_object_or_404(SaleItem, pk=item_pk, sale=sale)
    item.delete()
    
    # Update sale total
    sale.total = sum(item.quantity * item.price for item in sale.items.all())
    sale.save()
    
    if request.htmx:
        return render(request, 'sales/partials/sale_items.html', {'sale': sale})
    return redirect('sale_detail', pk=pk)
