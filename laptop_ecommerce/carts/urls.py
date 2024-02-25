from django.urls import path
from .views import *
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_cart/<int:product_id>/', AddCartView.as_view(), name='add_cart'),
    path('remove_cart/<int:product_id>/', RemoveCartView.as_view(), name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),

]