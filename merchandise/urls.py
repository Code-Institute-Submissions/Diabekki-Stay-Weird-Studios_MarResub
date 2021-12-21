from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_merchandise, name='merchandise'),
    path('<merch_id>/', views.merch_details, name='merch_details'),
]
