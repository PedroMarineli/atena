from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.views.static import serve
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

# Serve media files in development and production (if not handled by Nginx)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
