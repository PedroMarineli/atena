from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Product, Service, Supplier
from .forms import ProductForm, ServiceForm, SupplierForm

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form})

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form})

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_confirm_delete.html', {'supplier': supplier})

@login_required
def item_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/item_list.html', {'products': products, 'page_title': 'Produtos'})

@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'inventory/item_list.html', {'services': services, 'page_title': 'Serviços'})

@login_required
def item_create(request):
    # Simplified to Product for now to allow migrations
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                products = Product.objects.all()
                return render(request, 'inventory/partials/item_list_rows.html', {'products': products})
            return redirect('item_list')
    else:
        form = ProductForm()
    
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', {'form': form})
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_update(request, pk):
    # Simplified to Product for now
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if request.htmx:
                products = Product.objects.all()
                return render(request, 'inventory/partials/item_list_rows.html', {'products': products})
            return redirect('item_list')
    else:
        form = ProductForm(instance=item)
    
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', {'form': form, 'item': item})
    return render(request, 'inventory/item_form.html', {'form': form, 'item': item})

@login_required
@require_http_methods(["DELETE", "POST"])
def item_delete(request, pk):
    # Simplified to Product for now
    item = get_object_or_404(Product, pk=pk)
    item.delete()
    if request.htmx:
        products = Product.objects.all()
        return render(request, 'inventory/partials/item_list_rows.html', {'products': products})
    return redirect('item_list')
