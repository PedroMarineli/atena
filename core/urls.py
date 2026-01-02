from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls), # Admin site
    path('accounts/', include('django.contrib.auth.urls')), # Authentication routes
    path('inventory/', include('inventory.urls')), # Inventory management
    path('sales/', include('sales.urls')), # Sales management
    path('finance/', include('finance.urls')), # Finance management
    path('', include('dashboard.urls')), # Dashboard as the home page
]
