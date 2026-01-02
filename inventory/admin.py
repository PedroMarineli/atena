from django.contrib import admin
from .models import Product, Service, Supplier

admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Supplier)
