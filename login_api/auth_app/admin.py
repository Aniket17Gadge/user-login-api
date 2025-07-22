from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RegisteredEmail, OTP
from django.utils.translation import gettext_lazy as _
from django import forms


from django.contrib import admin
from .models import RegisteredEmail, OTP

@admin.register(RegisteredEmail)
class RegisteredEmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'hashed_otp', 'salt', 'created_at']
    list_filter = ['created_at']
    search_fields = ['email']
