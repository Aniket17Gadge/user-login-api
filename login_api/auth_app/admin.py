from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RegisteredEmail, OTP
from django.utils.translation import gettext_lazy as _
from django import forms


from django.contrib import admin
from .models import RegisteredEmail, OTP

#Useful for tracking which emails are registered in the system.
@admin.register(RegisteredEmail)
class RegisteredEmailAdmin(admin.ModelAdmin):
    list_display = ['email'] #Shows email field in list view.

    search_fields = ['email']#Allows search by email.

#monitor OTPs being generated 
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'hashed_otp', 'salt', 'created_at']
    list_filter = ['created_at']
    search_fields = ['email']
