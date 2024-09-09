from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from support_ticket_system_app.models import Ticket, Message, CustomUser
from support_ticket_system_app.serializers import TicketSerializer


@api_view(['GET'])
def get_ticket_list(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)

    return Response({'tickets': serializer.data})


@api_view(['GET'])
def ticket_details(request, ticket_id):
    ticket_query = Ticket.objects.filter(pk=ticket_id)

    if not ticket_query.exists():
        return Response({'error': 'Ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)

    ticket = ticket_query.first()
    serializer = TicketSerializer(ticket)

    return Response({'ticket': serializer.data})


@api_view(['POST'])
def create_ticket(request):
    data = request.data
    user_query = CustomUser.objects.filter(pk=data.get('user'))

    if not user_query.exists():
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = user_query.first()

    ticket = Ticket.objects.create(
        subject=data.get('subject'),
        departament=data.get('departament'),
        status=data.get('status'),
        priority=data.get('priority'),
        user=user,
    )

    message_data = data.get('message', {})
    Message.objects.create(
        text=message_data.get('text'),
        direction=message_data.get('direction'),
        ticket=ticket,
        user=user,
    )

    return Response({'success': 'Ticket and message created'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_ticket(request, ticket_id):
    data = request.data

    ticket_query = Ticket.object.filter(pk=ticket_id)
    user_query = CustomUser.objects.filter(pk=data.get('user'))

    if not ticket_query.exists():
        return Response({'error': 'Ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)

    ticket = ticket_query.first()

    if not user_query.exists():
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = user_query.first()

    message_data = data.get('message', {})
    new_message = Message.objects.create(
        text=message_data.get('text'),
        direction=message_data.get('direction'),
        ticket=ticket,
        user=user
    )

    ticket.update_date = now()
    ticket.save(update_fields=['update_date'])   # ???

    return Response({'success': 'Message added to ticket', 'message_id': new_message.id}, status=status.HTTP_200_OK)









