from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name='user'),
    path('purchase_history/<purchase_number>', views.purchase_history, name='purchase_history'),
]