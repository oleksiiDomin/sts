from django.shortcuts import get_object_or_404
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
    ticket = Ticket.objects.get(pk=ticket_id)
    serializer = TicketSerializer(ticket)
    return Response({'ticket': serializer.data})


@api_view(['POST'])
def create_ticket(request):
    data = request.data
    user = get_object_or_404(CustomUser, pk=data.get('user'))

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

    return Response({'success': 'Ticket and message created'}, status=201)


@api_view(['PATCH'])
def update_ticket(request, ticket_id):
    data = request.data

    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = get_object_or_404(CustomUser, id=data.get('user'))

    message_data = data.get('message', {})
    new_message = Message.objects.create(
        text=message_data.get('text'),
        direction=message_data.get('direction'),
        ticket=ticket,
        user=user
    )

    ticket.update_date = now()
    ticket.save()

    return Response({'success': 'Message added to ticket', 'message_id': new_message.id}, status=status.HTTP_200_OK)









