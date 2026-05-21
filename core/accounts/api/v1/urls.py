from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "api-v1"

urlpatterns = [
    path('send-verify-code/', views.SendVerificationCodeApiView.as_view() ,name='send-verify-code'),
    path('login-otp/', views.LoginWithOtpApiView.as_view(), name="login-otp"),

    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),

    path('user/', views.UserInfoApiView.as_view(), name='user-info'),
]

router = DefaultRouter()
router.register('address', views.UserAddressViewSet,'address')

urlpatterns += router.urls
