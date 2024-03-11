from django.urls import path
from .views import *
from user.views import Home

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userdashboard/', UserDashboardView.as_view(), name='userdashboard'),

    path('home/', Home.as_view(), name='home'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='ForgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>', Resetpassword_ValidateView.as_view(), name='resetpassword_validate'),
    path('resetPassword/', ResetPasswordView.as_view(), name='resetPassword'),

    path('userdashboard/my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('userdashboard/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('userdashboard/user_changePassword/', ChangePasswordView.as_view(), name='userprofile_changePassword'),
    path('userdashboard/my_orders_detailed_view/<int:order_id>/<int:pk>/', MyOrdersDetailedView.as_view(), name='my_orders_detailed_view'),
    path('userdashboard/user_order_cancel_view/<pk>/', UserOrderCancelView.as_view(), name='user_order_cancel_view'),
]