from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.api.v1.permissions import IsOwner
from .serializers import OrderSerializer
from payment.models import Order

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = OrderSerializer
    lookup_field = "order_id"
    lookup_url_kwarg = "order_id"

    http_method_names = ["get", "post"]

    
    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)


    
    

    

