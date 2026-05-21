from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TicketReply

@receiver(post_save, sender=TicketReply)
def change_ticket_step(sender, instance: TicketReply, created, **kwargs):

    if created:
        
        if instance.is_systemReply :
            instance.ticket.step = "Answered"
        
        else:
            instance.ticket.step = "Pending"
        
        instance.ticket.save()
