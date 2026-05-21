from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views 

app_name = "api-v1"

router = DefaultRouter()
router.register("order", views.OrderViewSet, "order")

urlpatterns = [
    
]

urlpatterns += router.urls
