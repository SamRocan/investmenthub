from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('client_admin/', views.client_admin, name='client_admin'),
    path('client_admin/add_product', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='client/login.html'), name='login')
]