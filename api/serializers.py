from rest_framework import serializers
from django.contrib.auth.models import User

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
    owner = serializers.ReadOnlyField(source='owner.username')
    ticket = serializers.SlugRelatedField(many=True, read_only=False, queryset=Ticket.objects.filter(orders=None),
                                          slug_field='serial_number')

    class Meta:
        model = Order
        fields = '__all__'


class ConfirmedOrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Order
        fields = '__all__'


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']
