from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import RegisteredEmail, OTP
from .serializers import RegisteredEmailSerializer, OTPRequestSerializer

class RegisterEmailView(APIView):
    def post(self, request):
        serializer = RegisteredEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Rate limiting: 5 OTPs/hour
            one_hour_ago = timezone.now() - timedelta(hours=1)
            recent_otps = OTP.objects.filter(email=email, created_at__gte=one_hour_ago)

            if recent_otps.count() >= 5:
                return Response({"message": "OTP request limit reached. Try again later."}, status=429)

            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)