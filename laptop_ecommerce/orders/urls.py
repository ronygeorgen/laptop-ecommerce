from django.urls import path
from . views import * 

urlpatterns = [
    path('place_order/',PlaceOrderView.as_view(), name='place_order'),
    path('payments/',PaymentsView.as_view(), name='payments'),
    path('order_complete/',OrderCompleteView.as_view(), name='order_complete'),
    path('cashondelivery/<str:order_number>/',CashOnDeliveryView.as_view(), name='cashondelivery'),
]