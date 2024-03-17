from django.urls import path
from . views import *

urlpatterns = [
    path('add_coupon/',AddCoupon.as_view(), name='add_coupon'),
]