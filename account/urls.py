from django.urls import path
from .views import RegisterView , LoginView , LogoutView, ResendOTPView, VerifyOTPView, AdminLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'), 
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),

]
