from django.urls import path
from .views import *
from user.views import Home

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', Home.as_view(), name='home'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='ForgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>', Resetpassword_ValidateView.as_view(), name='resetpassword_validate'),
    path('resetPassword/', ResetPasswordView.as_view(), name='resetPassword'),
]