from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
import pytest
from accounts.models import User, OtpCode


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def common_no_verified_user():
    return User.objects.create(phone= "09123456789")

@pytest.fixture
def common_verified_user():
    return User.objects.create(phone= "09987654321", is_verified=True)

@pytest.mark.django_db
class TestUserApi:
    
    def test_send_verify_code_with_valid_data(self, api_client):

        url = reverse("accounts:api-v1:send-verify-code")

        data = {
            "phone" : "09123456789"
        }

        response = api_client.post(url, data= data)

        assert response.status_code == 201

    def test_send_verify_code_with_invalid_data(self, api_client):

        url = reverse("accounts:api-v1:send-verify-code")

        data = {
            "phone" : "923456789"
        }

        response = api_client.post(url, data= data)

        assert response.status_code == 400

    def test_login_otp_with_valid_otp(self, api_client, common_no_verified_user):

        # Create otp code
        otp = OtpCode.objects.create(user = common_no_verified_user)

        url = reverse("accounts:api-v1:login-otp")

        # Try to login with valid otp code

        data = {
            "phone" : common_no_verified_user.phone,
            "otp_code" : otp.otp_code
        }

        response = api_client.post(url, data= data)

        assert response.status_code == 200

    def test_loging_otp_with_expired_otp(self, api_client, common_no_verified_user):
    
        # Create expired otp code
        otp = OtpCode.objects.create(user= common_no_verified_user)

        otp.expired_at = timezone.datetime(2000,1,1)
        otp.save()


        url = reverse("accounts:api-v1:login-otp")


        # Try to login with expired otp 
        data = {
            "phone" : common_no_verified_user.phone,
            "otp_code" : otp.otp_code
        }

        response = api_client.post(url, data= data)

        assert response.status_code == 400

    def test_loging_otp_with_invalid_otp(self, api_client, common_no_verified_user):

        # Create expired otp code
        otp = OtpCode.objects.create(user= common_no_verified_user)


        url = reverse("accounts:api-v1:login-otp")


        # Try to login with invalid otp 
        data = {
            "phone" : common_no_verified_user.phone,
            "otp_code" : 000000
        }

        response = api_client.post(url, data= data)

        assert response.status_code == 400
    
    def test_get_user_info_response_200_status(self, api_client, common_verified_user):

        url = reverse("accounts:api-v1:user-info")

        api_client.force_authenticate(user = common_verified_user)

        response = api_client.get(url)

        assert response.status_code == 200


    def test_update_user_info_response_200_status(self, api_client, common_verified_user):

        url = reverse("accounts:api-v1:user-info")

        api_client.force_authenticate(user= common_verified_user)

        data = {
            "email" : "test_update_info@test.com"
        }

        response = api_client.put(url, data=data)

        assert response.status_code == 200


    def test_update_user_info_response_400_status(self, api_client, common_verified_user):

        url = reverse("accounts:api-v1:user-info")
        
        api_client.force_authenticate(user= common_verified_user)

        data = {
            "email" : "test_update_info.test.com"
        }

        response = api_client.put(url, data=data)

        assert response.status_code == 400



    
