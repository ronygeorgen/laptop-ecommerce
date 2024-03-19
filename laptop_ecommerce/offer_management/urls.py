from django.urls import path
from . views import * 

urlpatterns = [
    path('category_offer/',CategoryOfferView.as_view(), name='category_offer'),
    path('category_offer/category_edit/<pk>/',CategoryEditView.as_view(), name='category_edit'),
    path('category_offer/soft_delete/<pk>/',SoftDeleteCategoryOfferView.as_view(), name='soft_delete'),
    
    path('product_offer/',ProductOfferView.as_view(), name='product_offer'),
    path('product_offer/product_edit/<pk>/',ProductEditView.as_view(), name='product_edit'),
    path('product_offer/soft_delete_product/<pk>/',SoftDeleteProductOfferView.as_view(), name='soft_delete_product'),
]
