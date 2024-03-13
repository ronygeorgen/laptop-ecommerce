from django.urls import path
from . views import *

urlpatterns = [
    path('dashboard/',Dashboard.as_view(), name='dashboard'),
    path('user_list/',UserManagementView.as_view(), name='user_list'),
    path('user_block/<pk>/',UserBlockView.as_view(), name='user_block'),
    path('user_unblock/<pk>/',UserUnblockView.as_view(), name='user_unblock'),
    path('order_list/',OrderList.as_view(), name='order_list'),
    path('order_cancel_approve/<pk>/',OrderCancelApprove.as_view(), name='order_cancel_approve'),
    path('sales_report/',SalesReportView.as_view(), name='sales_report'),
]