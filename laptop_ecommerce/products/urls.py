from django.urls import path
from . views import *
from myadmin.views import Dashboard

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('store/', ProductView.as_view(), {'store': True}, name='store-product-view'),
    path('',Dashboard.as_view(), name='dashboard'),
]