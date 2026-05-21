from django.contrib import admin
from .models import Ticket,  TicketReply

# Register your models here.

class TicketReplyInlineAdmin(admin.StackedInline):
    model = TicketReply
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'step', 'creator__phone', 'priority', 'created_at']
    search_fields = ['creator__phone', 'title',]
    list_display = ['priority', 'status', 'step']

    inlines = [TicketReplyInlineAdmin,]