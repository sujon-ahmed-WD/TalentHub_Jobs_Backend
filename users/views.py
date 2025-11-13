from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer, RegisterSerializer,VerifyOtpSerializer,ResendOtpSerializer,LoginSerializer,ForgotPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User registered successfully . Check terminal for OTP '},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        user=User.objects.all()
        serializer=RegisterSerializer(user,many=True)
        return Response(serializer.data)

class VerifyOtpView(APIView):
    def post(self,request):
     serializer=VerifyOtpSerializer(data=request.data)
     if serializer.is_valid():
        email=serializer.validated_data['email']
        otp=serializer.validated_data['otp']
        try:
            user=User.objects.get(email=email)
            if user.otp==otp:
                user.is_active=True
                user.save()
                return Response({'message':'OTP verified successfully'})
            return Response({'error','invalid OTP'},status=400)
        except User.DoesNotExist:
            return Response({'error':'User not found'},status=404)
     return Response(serializer.errors,status=404)


class ResendOtpView(APIView):
    def post(self,request):
        serializer=ResendOtpSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            try:
                user=User.objects.get(email=email)
                new_otp=str(random.randint(100000,999999))
                user.otp=new_otp
                user.save()
                print(f"New Otp for {user.email} is : {new_otp}") 
                return Response({"message":"OTP resent Successfully.checkYour Email"},status=status.HTTP_200_OK)
            except User.DoesNotExist:
                 return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'email':user.email,
                'role':user.role
            })
        return Response(serializer.errors,status=400)
    print("Login done")

class ForgotPasswordView(APIView):
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            try:
                user=User.objects.get(email=email)
                user.otp=str(random.randint(100000,999999))
                user.save()
                print(f"Password reset OTP for {email}:{user.otp}")
                return Response({'message':'OTP sent to terminal'})
            except User.DoesNotExist:
                return Response({'error':'User not found'},status=404)
        return Response(serializer.errors,status=400)
            

class ChangePasswordView(APIView):
    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            otp=serializer.validated_data['otp']
            new_password=serializer.validated_data['new_password']
            try:
                user=User.objects.get(email=email)
    
                if user.otp==otp:
                    user.set_password(new_password)
                    user.save()
                    return Response({'message':'Password changed successfully'})
                return Response({'error':'Invalid OTP'},status=400)
            except User.DoesNotExist:
                return Response({'error':'User not found'},status=400)
        return Response(serializer.errors,status=404)
    
class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message','Logout successfully'})
        except Exception:
            return Response({'error':'Invalid token'},status=400)
