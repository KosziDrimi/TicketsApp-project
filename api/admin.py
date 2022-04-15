from django.contrib import admin

from .models import Event, Image, Order, Price, Ticket, TicketType


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime']
    inlines = [ImageInline]


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'is_paid', 'is_valid']
    inlines = [TicketInline]


class TicketAdmin(admin.ModelAdmin):
    list_display = ['serial_number', '__str__', 'order']
    ordering = ['order']


admin.site.register(Event, EventAdmin)
admin.site.register(Image)
admin.site.register(Order, OrderAdmin)
admin.site.register(Price)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketType)
