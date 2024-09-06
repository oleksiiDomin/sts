from django.contrib import admin
from django.contrib.admin import ModelAdmin

from support_ticket_system_app.models import Ticket, Message, CustomUser


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    pass



@admin.register(Message)
class MessageAdmin(ModelAdmin):
    pass



@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    pass



