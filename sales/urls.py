from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('', views.sale_list, name='sale_list'),
    path('create/', views.sale_create, name='sale_create'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/update/', views.sale_update, name='sale_update'),
    path('<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('<int:pk>/add_item/', views.sale_add_item, name='sale_add_item'),
    path('<int:pk>/remove_item/<int:item_pk>/', views.sale_remove_item, name='sale_remove_item'),
    path('<int:pk>/finalize/', views.sale_finalize, name='sale_finalize'),
]
