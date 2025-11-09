from django.db import models
import random
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,name,phone,password=None,**extra_fields):
        if not email:
            raise ValueError("Email fields must be set")
        email=self.normalize_email('email')
        user=self.model(email=email,name=name,phone=phone,**extra_fields)
        user.set_password(password)
        user.otp=str(random.randint(1000000,999999))
        user.is_active=True
        user.save(self._db)
        return user
    def create_superuser(self,email,name,phone,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('role','admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email,name,phone,password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES=(
        ('user','User'),
        ('admin','Admin')
    )
    email=models.EmailField(unique=True)
    Name=models.CharField(max_length=20)
    phone=models.CharField(max_length=11, blank=True,null=True)
    role=models.CharField(max_length=10, choices=ROLE_CHOICES,default='user')
    otp=models.CharField(max_length=6,blank=True,null=True)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    USER_NAME_FIELD='email'
    REQUIRED_FIELDS=['Name','phone','otp']

