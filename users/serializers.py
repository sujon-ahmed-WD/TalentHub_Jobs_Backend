from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
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
    
    