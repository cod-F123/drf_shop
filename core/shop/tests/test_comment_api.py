from rest_framework.test import APIClient
from django.urls import reverse
from decimal import Decimal
from shop.models import Product, Category, Comment
from accounts.models import User
import pytest


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def common_product():
    category = Category.objects.create(name="test_category")
    return Product.objects.create(
        title = "test_product", 
        category= category, 
        description = "<p>test_description</p>", 
        image = "/media/upload/test/blob.png", 
        price= Decimal("1200")
        )

@pytest.fixture
def common_user():
    return User.objects.create(
        phone = "09123456789", 
        is_verified=True
        )

@pytest.mark.django_db
class TestProductApi:

    def test_get_list_response_200_status(self, api_client):

        url = reverse("shop:api-v1:product-list")

        response = api_client.get(url)

        assert response.status_code == 200

    def test_get_first_product_response_200_status(self, api_client, common_product):

        url = reverse("shop:api-v1:product-detail", args=[common_product.slug])

        response = api_client.get(url)

        assert response.status_code == 200

    def test_get_product_response_404_status(self,  api_client,):
        url = reverse("shop:api-v1:product-detail", args=["blob-bl0b-pr0duct"])

        response = api_client.get(url)

        assert response.status_code == 404

    def test_create_comment_for_a_product_with_valid_data(self, api_client, common_product, common_user):

            url = reverse("shop:api-v1:create-comment")

            data = {
                "product" : common_product.id,
                "rating" : 5,
                "content" : "test_comment"
            }

            api_client.force_authenticate(user = common_user)

            response = api_client.post(url, data=data)

            assert response.status_code == 201

    def test_create_comment_for_a_product_with_invalid_data(self, api_client, common_product, common_user):

            url = reverse("shop:api-v1:create-comment")

            data = {
                "product" : "",
                "rating" : 5,
                "content" : "test_comment"
            }

            api_client.force_authenticate(user = common_user)

            response = api_client.post(url, data=data)

            assert response.status_code == 400


        

