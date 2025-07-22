from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import RegisteredEmail, OTP
from .serializers import RegisteredEmailSerializer, OTPRequestSerializer,OTPVerifySerializer
from .utils import generate_jwt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

#Controls request/response logic how the post request handle and what get injson response all mechanism handle here

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
    
class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Get or create user (we assume users login only with email)
            user, _ = User.objects.get_or_create(email=email, defaults={"email": email})

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "OTP verified successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)