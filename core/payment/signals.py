from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from .models import OrderItem

@receiver(post_save, sender=OrderItem)
@transaction.atomic
def calculate_total_amount(sender, instance : OrderItem, created, **kwargs):

    if created:
        instance.amount = instance.product.offed_price * instance.quantity if instance.product.is_offed else instance.product.price * instance.quantity
        instance.save()

        instance.product.stock -= instance.quantity
        instance.product.save()

        instance.order.total_amount += instance.amount
        instance.order.save()

