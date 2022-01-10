from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_checkout, name='cart_checkout')
]