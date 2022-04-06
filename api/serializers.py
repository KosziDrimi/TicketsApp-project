from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Event, Order, Ticket


class EventSerializer(serializers.HyperlinkedModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_tickets(self, obj):
        return Ticket.objects.filter(event=obj.id, orders=None).values('price').annotate(tickets_number=Count('price')).\
            values('price__price', 'price__ticket_type__name', 'tickets_number')


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


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']
