from django.urls import path
from .views import *
from user.views import Home

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', Home.as_view(), name='home'),
]