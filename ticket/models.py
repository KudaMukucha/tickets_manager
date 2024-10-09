from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES =[
        ('Active','Active'),
        ('Pending','Pending'),
        ('Resolved','Resolved')
    ]
    SEVERITY_CHOICES =[
        ('High','High'),
        ('Low','Low')
    ]

    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer_tickets')
    engineer = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='engineer_tickets',null=True)
    ticket_id = models.CharField(max_length=20,unique=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=5,choices=SEVERITY_CHOICES,default='Low')
    is_assigned_to_engineer= models.BooleanField(default=False)
    resolution_steps = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.title


