from rest_framework.test import APIClient
from django.urls import reverse
from decimal import Decimal
from shop.models import Product, Category
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

        

