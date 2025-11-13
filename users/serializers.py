from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer): # ata and 
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['name','email','password','phone']
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )
        print(f"OTP for {user.email} {user.otp}")
        return user
    
class VerifyOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    

class ResendOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
    

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    
    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        user=authenticate(email=email,password=password)
        if user and user.is_active:
            data['user']=user
            return data
        raise serializers.ValidationError("Invalid credentials")
        
    
class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
class ChangePasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    new_password=serializers.CharField(write_only=True)

class AllvalueSerializer(serializers.ModelSerializer):

        class Meta:
            model=User
            fields='__all__'
