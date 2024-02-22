from django.urls import path
from . views import *
from myadmin.views import Dashboard

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('product_list/',ProductEdit.as_view(), name='product_list'),
    path('product_list/<pk>/',ProductEditView.as_view(), name='product_list_edit'),
    path('dashboard/',Dashboard.as_view(), name='dashboard'),
    path('product_delete/<pk>/',SoftDeleteProductView.as_view(), name='product_delete'),
]
