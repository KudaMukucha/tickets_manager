from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ticket.models import Ticket
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_customer:
        tickets = Ticket.objects.filter(customer = request.user)
        active_tickets = Ticket.objects.filter(customer = request.user,is_resolved = False)
        resolved_tickets = Ticket.objects.filter(customer = request.user,is_resolved = True)
        return render(request,'dashboard/customer-dashboard.html',{'tickets':tickets,'active_tickets':active_tickets,'resolved_tickets':resolved_tickets})
    elif request.user.is_engineer:
        tickets = Ticket.objects.filter(engineer = request.user)
        active_tickets = Ticket.objects.filter(engineer = request.user,is_resolved = False)
        resolved_tickets = Ticket.objects.filter(engineer = request.user,is_resolved = True)
        return render(request,'dashboard/engineer-dashboard.html',{'tickets':tickets,'active_tickets':active_tickets,'resolved_tickets':resolved_tickets})
    elif request.user.is_superuser:
        return render(request,'dashboard/adminstrator-dashboard.html')
    