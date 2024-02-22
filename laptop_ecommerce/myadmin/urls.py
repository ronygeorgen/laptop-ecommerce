from django.urls import path
from . views import *

urlpatterns = [
    path('dashboard/',Dashboard.as_view(), name='dashboard'),
    path('user_list/',UserManagementView.as_view(), name='user_list'),
    path('user_block/<pk>/',UserBlockView.as_view(), name='user_block'),
    path('user_unblock/<pk>/',UserUnblockView.as_view(), name='user_unblock'),
]