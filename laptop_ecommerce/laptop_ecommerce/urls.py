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
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('defaultadmin/', admin.site.urls),
    path('',include('user.urls')),
    path('admin/',include('myadmin.urls')),
    path('category/',include('category.urls')),
    path('',include('category.urls')),
    path('',include('category.urls')),
    path('product/',include('products.urls')),
    path('product_list/',include('products.urls')),
    path('variationsform/',include('products.urls')),
    path('dashboard/',include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('coupon/', include('coupon_Mng.urls')),
]