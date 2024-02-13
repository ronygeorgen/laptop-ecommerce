from django.urls import path
from . views import *
from myadmin.views import Dashboard

urlpatterns = [
    path('product/', ProductView.as_view(), name='product'),
    path('dashboard/',Dashboard.as_view(), name='Dashboard')
]