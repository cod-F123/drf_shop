from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.

class Ticket(models.Model):

    STATUS = (
        ("Open", "Open"),
        ("Close", "Close"),
    )

    STEP = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Answered", "Answered"),
    )

    PRIORITY = (
        ('Low', 'Low'),
        ("Medium", "Medium"),
        ("High", "High")
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=100)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ticket_id = models.CharField(max_length=255, blank=True, null=True, unique= True)

    priority = models.CharField(max_length=6, choices=PRIORITY, default="Medium")
    status = models.CharField(max_length=5, choices=STATUS, default="Open")
    step = models.CharField(max_length=10, choices=STEP, default="Pending")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        if not self.ticket_id:
            self.ticket_id = str(int(uuid.uuid4()))[:7]
        
        super().save(*args, **kwargs)


class TicketReply(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="replies")

    sender = models.ForeignKey(User, on_delete= models.CASCADE, related_name="ticket_replies")

    content = models.TextField()
    attach  = models.FileField(upload_to="tickets/attach", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_systemReply = models.BooleanField(default=False)

    def __str__(self):
        return self.ticket.ticket_id