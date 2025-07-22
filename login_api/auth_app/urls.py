# urls.py
from django.urls import path
from .views import RegisterEmailView,OTPRequestView,OTPVerifyView

#Routes frontend/API calls to backend logic. Routing to connect with ui or access specfic data by specfic url name

urlpatterns = [
    path('register/', RegisterEmailView.as_view(), name='register'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
]