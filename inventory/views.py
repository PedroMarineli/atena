from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse
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

def get_inventory_context():
    return {
        'products': Product.objects.all(),
        'services': Service.objects.all()
    }

@login_required
def item_list(request):
    context = get_inventory_context()
    context['page_title'] = 'Produtos'
    return render(request, 'inventory/item_list.html', context)

@login_required
def service_list(request):
    context = get_inventory_context()
    context['page_title'] = 'Serviços'
    return render(request, 'inventory/item_list.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
            return redirect('item_list')
    else:
        form = ProductForm()
    
    context = {'form': form, 'submit_url': reverse('item_create'), 'modal_title': 'Novo Produto'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
def item_update(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
            return redirect('item_list')
    else:
        form = ProductForm(instance=item)
    
    context = {'form': form, 'item': item, 'submit_url': reverse('item_update', args=[item.pk]), 'modal_title': 'Editar Produto'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
@require_http_methods(["DELETE", "POST"])
def item_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item.delete()
    if request.htmx:
        return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
    return redirect('item_list')

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
            return redirect('service_list')
    else:
        form = ServiceForm()
    
    context = {'form': form, 'submit_url': reverse('service_create'), 'modal_title': 'Novo Serviço'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    
    context = {'form': form, 'item': service, 'submit_url': reverse('service_update', args=[service.pk]), 'modal_title': 'Editar Serviço'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
@require_http_methods(["DELETE", "POST"])
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    if request.htmx:
        return render(request, 'inventory/partials/item_list_rows.html', get_inventory_context())
    return redirect('service_list')
