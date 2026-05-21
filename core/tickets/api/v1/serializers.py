from rest_framework import serializers
from django.contrib.auth import get_user_model
from tickets.models import Ticket, TicketReply

class UserTicketSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField("get_full_name", read_only=True)

    def get_full_name(self, obj):
        return obj.profile.full_name

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'id']

class TicketReplySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only = True)


    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['sender'] = UserTicketSerializer(instance.sender).data

        return rep
    
    def create(self, validated_data):

        validated_data["sender"] = self.context["request"].user

        return super().create(validated_data)

    class Meta:
        model = TicketReply
        fields = ["id", "sender", "is_systemReply", "content", "attach", "created_at", "ticket"]
        read_only_fields = ["id", "is_systemReply", "created_at", 'sender']


class TicketSerializer(serializers.ModelSerializer):

    replies = TicketReplySerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only = True)
    updated_at = serializers.DateTimeField("%Y/%m/%d %H:%M", read_only = True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        rep['creator'] = UserTicketSerializer(instance.creator).data

        request = self.context["request"]

        if not request.parser_context.get("kwargs").get("ticket_id"):
            rep.pop("replies")
            rep.pop("content")
            

        return rep
    
    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user

        return super().create(validated_data)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id',"title", 'creator', 'content', 'status', 'step', 'priority', 'created_at', 'updated_at', 'replies']
        read_only_fields = ['id', 'ticket_id', 'creator', 'status', 'step', 'created_at', 'updated_at']