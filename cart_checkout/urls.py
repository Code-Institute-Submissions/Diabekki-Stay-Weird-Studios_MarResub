from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_checkout, name='cart_checkout'),
    path('cart_checkout_success/<purchase_number>', views.cart_checkout_success, name='cart_checkout_success'),
]