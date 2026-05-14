from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import Product 
from .serializers import ProductSerializer
from .paginations import DefaultPagination

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category',]
    ordering_fields = ['discount', 'price', 'added_at'] 
    search_fields = ['$title', '$category__name' ]   
    pagination_class = DefaultPagination
    