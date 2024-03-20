from django.urls import path
from . views import *

urlpatterns = [
    path('add_coupon/',AddCoupon.as_view(), name='add_coupon'),
    path('edit_coupon/<pk>',EditCouponView.as_view(), name='edit_coupon'),
    path('delete_coupon/<pk>',DeleteCouponView.as_view(), name='delete_coupon'),
]