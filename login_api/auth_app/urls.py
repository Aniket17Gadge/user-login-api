# urls.py
from django.urls import path
from .views import RegisterEmailView,OTPRequestView,OTPVerifyView

urlpatterns = [
    path('register/', RegisterEmailView.as_view(), name='register'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
]