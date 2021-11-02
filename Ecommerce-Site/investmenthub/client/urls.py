from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from . import views
urlpatterns = [
    path('client_admin/', views.client_admin, name='client_admin'),
    path('client_admin/orders/<int:page>/', views.client_orders, name='client_orders'),
    path('client_admin/products/<int:page>/', views.client_products, name='client_products'),
    path('client_admin/add_product', views.add_product, name='add_product'),
    path('client_admin/edit_product/<slug:product_slug>', views.edit_product, name='edit_product'),
    path('client_admin/delete_product/<slug:product_slug>', views.delete_product, name='delete_product'),
    path('graphs/', views.ChartData.as_view(), name='ChartData'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='client/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='client/login.html', authentication_form=UserLoginForm), name='login')
]