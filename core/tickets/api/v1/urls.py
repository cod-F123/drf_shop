from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views 

app_name = "api-v1"

urlpatterns = [
    path('reply-ticket/' , views.CreateReplyTicket.as_view(), name="create-reply-ticket")
]

router = DefaultRouter()
router.register('ticket', views.TicketViewSet, 'ticket')

urlpatterns += router.urls