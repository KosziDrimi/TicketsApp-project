from django.db import models


class TicketType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name


class Price(models.Model):
    price = models.FloatField()
    ticket_type = models.ForeignKey(TicketType, related_name='prices', on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, related_name='prices', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.price} EUR'


class Ticket(models.Model):
    serial_number = models.CharField(max_length=20, unique=True)
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.DO_NOTHING)
    price = models.ForeignKey(Price, related_name='tickets', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.price.ticket_type} - {self.price} EUR - {self.event}'


class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    is_paid = models.BooleanField(default=False)
    order_datetime = models.DateTimeField(auto_now_add=True)
    ticket = models.ManyToManyField(Ticket, related_name='orders')
    owner = models.ForeignKey('auth.User', related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.order_number
