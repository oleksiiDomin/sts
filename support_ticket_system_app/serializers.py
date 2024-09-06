from rest_framework.serializers import ModelSerializer

from support_ticket_system_app.models import Ticket, Message, CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'



class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['uuid', 'text', 'direction', 'create_date']



class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['uuid', 'subject', 'departament', 'status', 'priority', 'create_date', 'update_date', 'user', 'messages']

    messages = MessageSerializer(many=True, read_only=True)


