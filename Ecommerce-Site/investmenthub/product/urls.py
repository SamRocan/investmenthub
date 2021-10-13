from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('search/', views.product_home, name='product_search'),
    path('<slug:product_slug>/', views.product_page, name='product_page')
]