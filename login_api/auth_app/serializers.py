from rest_framework import serializers
from .models import RegisteredEmail, OTP
import secrets
import hashlib

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
