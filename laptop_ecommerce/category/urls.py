from django.urls import path
from . views import *
from products.views import ProductView

urlpatterns = [
    path('category/',CategoryView.as_view(), name='category'),
    path('edit_category/<pk>/',EditView.as_view(), name='edit_category'),
    path('soft_delete_category/<pk>/',SoftDeleteCategoryView.as_view(), name='soft_delete_category'),
]