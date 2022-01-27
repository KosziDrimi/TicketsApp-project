from rest_framework import serializers

from .models import TicketType, Event, Price, Order, Ticket


class TicketTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):
    tickets = serializers.StringRelatedField(many=True)

    class Meta:
        model = Event
        fields = '__all__'


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
