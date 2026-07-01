from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from accounts.models import AddressUser
from shop.models import Product

User = get_user_model()

# Create your models here.

class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Payed', 'Payed'),
        ('Sent', 'Sent'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=15, decimal_places=0)

    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=7, choices=STATUS, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    payed_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    order_id = models.CharField(max_length=191, blank=True, null=True)

    def __str__(self):
        return self.user.phone

    def save(self, *args, **kwargs):

        if not self.order_id:
            self.order_id = str(uuid.uuid4().int)[:7] 


        if self.status == 'Payed' and not self.payed_at:
            self.payed_at = timezone.now()

        if self.status == 'Sent' and not self.sent_at:
            self.sent_at = timezone.now()


        super().save(*args, **kwargs)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=1)

    amount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return f"{self.order.order_id} - {self.product.title}"
    
