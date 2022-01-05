from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<merch_id>/', views.shopping_cart_quantity, name='shopping_cart_quantity'),
]
