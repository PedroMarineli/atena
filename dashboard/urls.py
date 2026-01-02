from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'), # Dashboard home
    path('users/create/', views.user_create, name='user_create'), # Create a new user
]
