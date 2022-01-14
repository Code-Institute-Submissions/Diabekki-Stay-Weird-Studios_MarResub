from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_merchandise, name='merchandise'),
    path('<int:merch_id>/', views.merch_details, name='merch_details'),
    path('add/', views.add_merch, name='add_merch'),
    path('edit/<int:merch_id>/', views.edit_merch, name='edit_merch'),
]
