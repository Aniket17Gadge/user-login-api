# urls.py
from django.urls import path
from .views import RegisterEmailView,OTPRequestView

urlpatterns = [
    path('register/', RegisterEmailView.as_view(), name='register'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
]