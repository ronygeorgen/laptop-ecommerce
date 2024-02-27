from django.urls import path
from . views import * 

urlpatterns = [
    path('place_order/',PlaceOrderView.as_view(), name='place_order'),
]