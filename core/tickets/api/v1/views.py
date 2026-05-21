from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTicketOrwner
from tickets.models import Ticket, TicketReply
from .serializers import TicketSerializer, TicketReplySerializer

class TicketViewSet( mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet,):

    permission_classes = [IsAuthenticated, IsTicketOrwner,]
    serializer_class = TicketSerializer

    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"
    

    def get_queryset(self):
        return Ticket.objects.filter(creator__id = self.request.user.id)

class CreateReplyTicket(generics.CreateAPIView):
    serializer_class = TicketReplySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return TicketReply.objects.filter(ticket__creator = self.request.user)

    