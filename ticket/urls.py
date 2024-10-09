from django.urls import path
from .import views

app_name = 'ticket'

urlpatterns =[
    path('create-ticket/',views.create_ticket,name='create-ticket'),
    path('active-customer-tickets/',views.active_customer_tickets,name='active-customer-tickets'),
    path('resolved-customer-tickets/',views.resolved_customer_tickets,name='resolved-customer-tickets'),
    path('assign-ticket/<int:ticket_id>/',views.assign_ticket,name='assign-ticket'),
    path('ticket-details/<int:ticket_id>/',views.ticket_details,name='ticket-details'),
    path('ticket-queue/',views.ticket_queue,name='ticket-queue'),
    path('active-engineer-tickets/',views.active_engineer_tickets,name='active-engineer-tickets'),
    path('resolved-engineer-tickets/',views.resolved_engineer_tickets,name='resolved-engineer-tickets'),
    path('resolve-ticket/<int:ticket_id>/',views.resolve_ticket,name='resolve-ticket'),
    path('ticket-search/',views.search_ticket,name='ticket-search')
]