from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path('send-verify-code/', views.SendVerificationCodeApiView.as_view() ,name='send-verify-code'),
    path('login-otp/', views.LoginWithOtpApiView.as_view(), name="login-otp"),

    path('user/', views.UserInfoApiView.as_view(), name='user-info'),
]
