from datetime import timedelta, timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from notification.views import register_fcm_token
from .models import CustomUser, OTP
from .serializers import RegisterSerializer
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import UserState
from decimal import Decimal
from .models import Wallet, WalletTransaction
from .serializers import WalletTopUpSerializer , WalletSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

def send_otp_email(email, otp_code):
    subject = '🔐 Verify your HomeWorkout Account with this OTP'
    from_email = 'homeworkout308@gmail.com'
    to = [email]

    # HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px;">
        <h2 style="color: #8a4fff; text-align: center;">Welcome to <span style="color:#333;">HomeWorkout</span>! 💪</h2>
        <p style="font-size: 16px; color: #444;">Thanks for signing up!</p>
        <p style="font-size: 16px; color: #444;">Your One-Time Password (OTP) is:</p>
        <div style="font-size: 24px; font-weight: bold; color: #8a4fff; text-align: center; margin: 20px 0;">
            {otp_code}
        </div>
        <p style="font-size: 14px; color: #666;">This code will expire in a few minutes.</p>
        <hr style="margin: 30px 0;">
        <p style="font-size: 12px; color: #999;">If you didn’t request this, just ignore this email.</p>
        <p style="font-size: 14px; color: #444;">– The HomeWorkout Team</p>
        </div>
    </body>
    </html>
    """
    text_content = f"""Thanks for signing up for HomeWorkout!
Your OTP is: {otp_code}
This code will expire in a few minutes.
If you didn’t request this, ignore this message.
"""
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()




class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_obj, created = OTP.objects.get_or_create(user=user)
            otp_obj.generate_code()
            send_otp_email(user.email, otp_obj.code)
            return Response({"message": "User registered successfully. Please verify your email using the OTP sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('otp')
        if not email or not code:
            return Response({"error": "Email and OTP code are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = OTP.objects.get(user=user)
            if otp_obj.code != code:
                return Response({"error": "❌ Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
                return Response({"error": "⏰ OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            otp_obj.delete()
            return Response({"message": "✅ OTP verified successfully!"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return Response({"error": "OTP not found for this user"}, status=status.HTTP_404_NOT_FOUND)



class ResendOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            otp, created = OTP.objects.get_or_create(user=user)
            otp.generate_code() 
            send_otp_email(user.email, otp.code)
            return Response({"message": "OTP has been resent."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        fcm_token = request.data.get('fcm_token')
        if email is None or password is None:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        register_fcm_token(user, fcm_token)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=200)
    

from django.contrib.auth import get_user_model
User = get_user_model()
class AdminLoginView(APIView):
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"detail": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_superuser:
            return Response({"detail": "Access denied. Only superuser can login here."}, status=status.HTTP_403_FORBIDDEN)
        # generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    

class UserStateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_state = UserState.objects.get(user=request.user)
        except UserState.DoesNotExist:
            return Response({"message": "User state not found"}, status=status.HTTP_404_NOT_FOUND)

        bmi = user_state.bmi
        if bmi:
            if bmi < 18.5:
                status_text = "Underweight"
            elif 18.5 <= bmi < 25:
                status_text = "Normal"
            elif 25 <= bmi < 30:
                status_text = "Overweight"
            else:
                status_text = "Obese"
            bmi_display = f"{bmi} ({status_text})"
        else:
            bmi_display = "BMI not available"

        return Response({
            "total_calories": user_state.total_calories,
            "total_minutes": round(user_state.total_minutes, 2) if user_state.total_minutes is not None else None,
            "bmi": bmi_display
        })


User = get_user_model()

class WalletAPIView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = WalletTopUpSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            amount = serializer.validated_data['amount']
            description = serializer.validated_data['description']

            try:
                user = User.objects.get(id=user_id)
                wallet, created = Wallet.objects.get_or_create(user=user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            wallet.balance += Decimal(amount)  
            wallet.save()
            
            WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='CREDIT',
                description=description
            )

            return Response({
                "message": "Wallet topped up successfully",
                "new_balance": wallet.balance
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WalletDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
