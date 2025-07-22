from rest_framework import serializers
from .models import RegisteredEmail, OTP
import secrets
import hashlib
from django.utils import timezone
from datetime import timedelta

class RegisteredEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredEmail
        fields = ['email']

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def create(self, validated_data):
        return RegisteredEmail.objects.create(**validated_data)

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not RegisteredEmail.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not registered.")
        return value

    def generate_secure_otp(self):
        return secrets.randbelow(900000) + 100000  # 6-digit OTP

    def generate_salt(self):
        return secrets.token_hex(4)  # 8 char = 4 bytes

    def hash_otp(self, otp, salt):
        return hashlib.sha256(f"{otp}{salt}".encode()).hexdigest()

    def create(self, validated_data):
        email = validated_data['email']
        otp = self.generate_secure_otp()
        salt = self.generate_salt()
        otp_hash = self.hash_otp(otp, salt)

        # Save the OTP with hash and salt
        OTP.objects.create(email=email, hashed_otp=otp_hash, salt=salt)

        # Mock send OTP
        print(f"[MOCK EMAIL] OTP for {email}: {otp}")

        return {"message": "OTP sent to your email (printed in console)."}

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        otp = data['otp']

        # Fetch latest OTP record
        try:
            record = OTP.objects.filter(email=email).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("No OTP request found for this email.")

        # Check if OTP is expired (e.g., 10 min)
        if timezone.now() - record.created_at > timedelta(seconds=20):
            raise serializers.ValidationError("OTP expired.")

        # Hash the input OTP with the saved salt and compare
        otp_hash = hashlib.sha256(f"{otp}{record.salt}".encode()).hexdigest()
        if otp_hash != record.hashed_otp:
            raise serializers.ValidationError("Invalid OTP.")

        return data
