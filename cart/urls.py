from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path(
        'shopping/<merch_id>/',
        views.shopping_cart_quantity, name='shopping_cart_quantity'),
    path('change/<merch_id>/', views.change_cart, name='change_cart'),
    path('remove/<merch_id>/', views.remove_merch, name='remove_merch'),
]
