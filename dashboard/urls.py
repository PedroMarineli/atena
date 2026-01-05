from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('charts-data/', views.dashboard_charts_data, name='dashboard_charts_data'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('organization/', views.organization_update, name='organization_update'),
]
