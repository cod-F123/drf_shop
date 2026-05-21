from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api-v1'

router = DefaultRouter()

router.register('product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('special-suggestion/', views.SpecialSuggestionApiView.as_view(), name="special-suggestion"),
    path('comment/create/', views.CreateCommentApiView.as_view(), name="create-comment"),
]

urlpatterns += router.urls

