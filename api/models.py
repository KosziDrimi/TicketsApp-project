from datetime import timedelta
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.timezone import localtime
from rest_framework import serializers


def simple_serializer(cls):
    class SimpleSerializer(serializers.ModelSerializer):
        class Meta:
            model = cls
            exclude = ('id',)

    cls.SimpleSerializer = SimpleSerializer
    return cls


@simple_serializer
class TicketType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name


@simple_serializer
class Price(models.Model):
    price = models.FloatField()
    ticket_type = models.ForeignKey(TicketType, related_name='prices', on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, related_name='prices', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.price} EUR - {self.ticket_type} - {self.event}'


class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_paid = models.BooleanField(default=False)
    order_datetime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order_number}'

    @property
    def is_valid(self):
        return (localtime() - self.order_datetime < timedelta(minutes=10)) or self.is_paid


@simple_serializer
class Ticket(models.Model):
    serial_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    price = models.ForeignKey(Price, related_name='tickets', on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, related_name='tickets', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'<{self.price}>'


@simple_serializer
class Image(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(['jpeg', 'jpg', 'png'])])
    event = models.ForeignKey(Event, related_name='images', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title
