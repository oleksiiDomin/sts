from django.urls import path

from support_ticket_system_app import views



urlpatterns = [
    path('', views.get_ticket_list, name='get_ticket_list'),
    path('<int:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
]