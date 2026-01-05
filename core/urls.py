from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # Admin site
    path('accounts/', include('django.contrib.auth.urls')), # Authentication routes
    path('inventory/', include('inventory.urls')), # Inventory management
    path('sales/', include('sales.urls')), # Sales management
    path('finance/', include('finance.urls')), # Finance management
    path('', include('dashboard.urls')), # Dashboard as the home page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
