from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('product/', views.product_home, name='product_home')
]