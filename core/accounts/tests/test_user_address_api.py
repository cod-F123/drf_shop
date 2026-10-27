from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
import pytest
from accounts.models import User, AddressUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    return User.objects.create(phone="09123456789", is_verified=True)


@pytest.fixture
def common_address(common_user):
    return AddressUser.objects.create(user=common_user, title="address_api_test", address="test_address_api", zip_code="0123456789")


@pytest.mark.django_db
class TestUserAddressApi:

    def test_get_address_list_response_200_status(self, api_client, common_user):

        url = reverse("accounts:api-v1:address-list")

        api_client.force_authenticate(user=common_user)

        response = api_client.get(url)

        assert response.status_code == 200

    def test_create_address_response_201_status(self, api_client, common_user):

        url = reverse("accounts:api-v1:address-list")

        api_client.force_authenticate(user=common_user)

        data = {
            "title": "test_address_api",
            "address": "test_address_api",
            "zip_code": "0192945898"
        }

        response = api_client.post(url, data=data)

        assert response.status_code == 201

    def test_create_address_response_400_status(self, api_client, common_user):

        url = reverse("accounts:api-v1:address-list")

        api_client.force_authenticate(user=common_user)

        data = {
            "title": "test_address_api",
            "zip_code": "1929458"
        }

        response = api_client.post(url, data=data)

        assert response.status_code == 400

    def test_update_address_reponse_200_status(self, api_client, common_user, common_address):

        url = reverse("accounts:api-v1:address-detail",
                      args=[common_address.id])

        api_client.force_authenticate(user=common_user)

        data = {
            "title": "address_api_test_updated",
            "address": "test_address_api",
            "zip_code": "9876543210"
        }

        response = api_client.put(url, data=data)

        assert response.status_code == 200
