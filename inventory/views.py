from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.db import models
from .models import Product, Service, Supplier
from .forms import ProductForm, ServiceForm, SupplierForm
from dashboard.views import is_admin

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
            if request.htmx:
                suppliers = Supplier.objects.all()
                return render(request, 'inventory/partials/supplier_list_rows.html', {'suppliers': suppliers})
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    context = {'form': form, 'submit_url': reverse('supplier_create'), 'modal_title': 'Novo Fornecedor'}
    if request.htmx:
        return render(request, 'inventory/partials/supplier_form.html', context)
    return render(request, 'inventory/supplier_form.html', context)

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            if request.htmx:
                suppliers = Supplier.objects.all()
                return render(request, 'inventory/partials/supplier_list_rows.html', {'suppliers': suppliers})
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    context = {'form': form, 'submit_url': reverse('supplier_update', args=[pk]), 'modal_title': 'Editar Fornecedor'}
    if request.htmx:
        return render(request, 'inventory/partials/supplier_form.html', context)
    return render(request, 'inventory/supplier_form.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE", "POST"])
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    try:
        supplier.delete()
        messages.success(request, 'Fornecedor excluído com sucesso.')
    except models.ProtectedError:
        messages.error(request, 'Não é possível excluir este fornecedor pois existem produtos associados a ele.')

    if request.htmx:
        suppliers = Supplier.objects.all()
        rows_html = render_to_string('inventory/partials/supplier_list_rows.html', {'suppliers': suppliers}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        final_html = rows_html + f'<tr style="display:none"><td>{messages_html}</td></tr>'
        return HttpResponse(final_html)
    return redirect('supplier_list')

@login_required
def item_list(request):
    context = {'products': Product.objects.all()}
    context['page_title'] = 'Produtos'
    return render(request, 'inventory/product_list.html', context)

@login_required
def service_list(request):
    context = {'services': Service.objects.all()}
    context['page_title'] = 'Serviços'
    return render(request, 'inventory/service_list.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/product_list_rows.html', {'products': Product.objects.all()})
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
                return render(request, 'inventory/partials/product_list_rows.html', {'products': Product.objects.all()})
            return redirect('item_list')
    else:
        form = ProductForm(instance=item)
    
    context = {'form': form, 'item': item, 'submit_url': reverse('item_update', args=[item.pk]), 'modal_title': 'Editar Produto'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE", "POST"])
def item_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    try:
        item.delete()
        messages.success(request, 'Produto excluído com sucesso.')
    except models.ProtectedError:
        messages.error(request, 'Não é possível excluir este produto pois existem vendas associadas a ele.')

    if request.htmx:
        rows_html = render_to_string('inventory/partials/product_list_rows.html', {'products': Product.objects.all()}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        final_html = rows_html + f'<tr style="display:none"><td>{messages_html}</td></tr>'
        return HttpResponse(final_html)
    return redirect('item_list')

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return render(request, 'inventory/partials/service_list_rows.html', {'services': Service.objects.all()})
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
                return render(request, 'inventory/partials/service_list_rows.html', {'services': Service.objects.all()})
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    
    context = {'form': form, 'item': service, 'submit_url': reverse('service_update', args=[service.pk]), 'modal_title': 'Editar Serviço'}
    if request.htmx:
        return render(request, 'inventory/partials/item_form.html', context)
    return render(request, 'inventory/item_form.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["DELETE", "POST"])
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    try:
        service.delete()
        messages.success(request, 'Serviço excluído com sucesso.')
    except models.ProtectedError:
        messages.error(request, 'Não é possível excluir este serviço pois existem vendas associadas a ele.')

    if request.htmx:
        rows_html = render_to_string('inventory/partials/service_list_rows.html', {'services': Service.objects.all()}, request=request)
        messages_html = render_to_string('partials/messages.html', {}, request=request)
        final_html = rows_html + f'<tr style="display:none"><td>{messages_html}</td></tr>'
        return HttpResponse(final_html)
    return redirect('service_list')
