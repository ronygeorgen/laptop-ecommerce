"""
URL configuration for laptop_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('store/',Store.as_view(), name='store-product-view'),
    path('store/category/<slug:category_slug>/',SlugStore.as_view(), name='product_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/<int:variation_id>/',ProductDetailView.as_view(), name='product_detail'),
    path('store/search/', SearchView.as_view(), name='search'),
    path('get_variant_details/', GetVariantDetailsView.as_view(), name='get_variant_details'),

    path('api/product-details/', GetSecondVariant.as_view(), name='get_second_product_details'),


    path('add_to_wishlist/<variation_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove_wishlist/<variation_id>/', RemoveWishlistView.as_view(), name='remove_wishlist'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]