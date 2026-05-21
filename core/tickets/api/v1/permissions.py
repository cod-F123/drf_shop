from rest_framework.permissions import BasePermission

class IsTicketOrwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator.id == request.user.id