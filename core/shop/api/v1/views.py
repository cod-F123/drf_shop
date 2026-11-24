from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import Product , SpecialSuggestion, Comment
from .serializers import ProductSerializer, SpecialSuggestionSerilaizer, CommentSerializer
from .paginations import DefaultPagination

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category").prefetch_related("comments").prefetch_related("galary").prefetch_related("Specifications")
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category__name', 'tag']
    ordering_fields = ['discount', 'price', 'added_at'] 
    search_fields = ['$title', '$category__name' ]   
    pagination_class = DefaultPagination


class CreateCommentApiView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related("user").select_related("product").all()


class SpecialSuggestionApiView(RetrieveAPIView):
    serializer_class = SpecialSuggestionSerilaizer
    
    def get_object(self):
        return SpecialSuggestion.objects.prefetch_related("products").filter(is_active=True).first()
    