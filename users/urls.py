from django.urls import path
from .views import RegisterView,VerifyOtpView,LoginView,ForgotPasswordView,ChangePasswordView,LogoutView
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('register/get/',RegisterView.as_view(),name='get'),
    path('verify-otp/',VerifyOtpView.as_view(),name='verify-otp'),
    path('login/',LoginView.as_view(),name='loginview'),
    path('forgot-password/',ForgotPasswordView.as_view(),name='forgot_password'),
    path('changepassword/',ChangePasswordView.as_view(),name='ChangePasswordview'),
    path('logout/',LogoutView.as_view(),name='logoutview')
    
]
