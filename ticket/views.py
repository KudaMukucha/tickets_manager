from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CreateTicketForm,AssignTicketForm
from .models import Ticket
import random
import string
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q 

# Create your views here.
User = get_user_model()

def create_ticket(request):
    ticket = None
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            while not ticket.ticket_id:
                id = ''.join(random.choices(string.digits,k=4))
                try:
                    ticket.ticket_id =id
                    ticket.save()
                    break
                except IntegrityError:
                    continue
            subject =f'{ticket.title} - #{ticket.ticket_id}'
            message = 'Thank you for creating a ticket, we will assign an engineer soon.'
            email_from = 'kudamukucha@gmail.com'
            recipient_list = [request.user.email,]
            send_mail(subject,message,email_from,recipient_list)
            messages.success(request,'Your ticket has been submitted. A support engineer would reach out soon.')
            return redirect('ticket:active-customer-tickets')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again!')
            return redirect('ticket:create-ticket')
    else:
        form = CreateTicketForm()
        return render(request,'ticket/create-ticket.html',{'form':form})

@login_required
def active_customer_tickets(request):
    ticket_list = Ticket.objects.filter(customer=request.user, is_resolved =False).order_by('-created')
    paginator = Paginator(ticket_list,6)
    page_number = request.GET.get('page',1)
    try:
        tickets = paginator.page(page_number)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    return render(request,'ticket/active-customer-tickets.html',{'tickets':tickets})

def resolved_customer_tickets(request):
    ticket_list = Ticket.objects.filter(customer=request.user, is_resolved = True).order_by('-created')
    paginator = Paginator(ticket_list,6)
    page_number = request.GET.get('page',1)
    try:
        tickets = paginator.page(page_number)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    return render(request,'ticket/resolved-customer-tickets.html',{'tickets':tickets})


def active_engineer_tickets(request):
    ticket_list = Ticket.objects.filter(engineer=request.user, is_resolved =False).order_by('-created')
    paginator = Paginator(ticket_list,6)
    page_number = request.GET.get('page',1)
    try:
        tickets = paginator.page(page_number)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    return render(request,'ticket/active-engineer-tickets.html',{'tickets':tickets})

def resolved_engineer_tickets(request):
    ticket_list = Ticket.objects.filter(engineer=request.user, is_resolved = True).order_by('-created')
    paginator = Paginator(ticket_list,6)
    page_number = request.GET.get('page',1)
    try:
        tickets = paginator.page(page_number)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    return render(request,'ticket/resolved-engineer-tickets.html',{'tickets':tickets})

def assign_ticket(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST,instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.is_assigned_to_engineer = True
            ticket.status = 'Active'
            ticket.save()
            messages.success(request,f'Ticket has been assigned to {ticket.engineer}')
            return redirect('ticket:ticket-queue')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again!')
            return redirect('ticket:assign-ticket')
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(is_engineer = True)
        return render(request,'ticket/assign-ticket.html',{'form':form,'ticket':ticket})

def ticket_details(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    return render(request,'ticket/ticket-details.html',{'ticket':ticket})

def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False)
    return render(request,'ticket/ticket-queue.html',{'tickets':tickets})

def resolve_ticket(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request,'Ticket is now resolved and closed')
        return redirect('dashboard:dashboard')

def search_ticket(request):
    query = request.GET.get('q')
    if request.user.is_customer:
        tickets = Ticket.objects.filter(customer=request.user).order_by('-created')
    elif request.user.is_engineer:
        tickets = Ticket.objects.filter(engineer=request.user).order_by('-created')

    if query:
        tickets = tickets.filter(
            Q(title__contains=query) |
            Q(ticket_id__contains = query) |
            Q(description__contains =query)
        )
    return render(request,'ticket/results.html',{'tickets':tickets,'query':query})

    