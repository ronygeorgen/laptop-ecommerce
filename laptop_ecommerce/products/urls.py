from django.urls import path
from . views import *
from myadmin.views import Dashboard

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('',Dashboard.as_view(), name='dashboard'),
]
