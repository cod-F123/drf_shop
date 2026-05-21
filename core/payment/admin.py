from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInlineAdmin(admin.StackedInline):
    model = OrderItem
    extra = 1 

    verbose_name_plural = "Order Items"
    verbose_name = "Order item"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'total_amount', 'user__phone', 'status', 'created_at']
    search_fields = ['order_id', 'user__phone', 'user__email']

    list_filter = ['status',]

    inlines = [OrderItemInlineAdmin,]