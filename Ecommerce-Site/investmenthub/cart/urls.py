from django.contrib import admin
from django.urls import path
from . import views
from .views import OrderCompleted
urlpatterns = [
  path('', views.cart_detail, name='cart'),
  path('completed/', OrderCompleted.as_view(), name="posts-requested"),
]