# Generated by Django 4.2.7 on 2024-10-07 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_alter_ticket_engineer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='contact_mode',
        ),
    ]
