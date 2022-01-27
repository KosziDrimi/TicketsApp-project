from django.contrib import admin

from .models import TicketType, Event, Price, Order, Ticket


admin.site.register(TicketType)
admin.site.register(Event)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(Ticket)
