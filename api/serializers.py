from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import serializers

from .models import Event, Order, Ticket


class EventSerializer(serializers.HyperlinkedModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_tickets(self, obj):
        return Ticket.objects.filter(price__event=obj.id, order=None).count()


class DetailEventSerializer(serializers.HyperlinkedModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_tickets(self, obj):
        return Ticket.objects.filter(price__event=obj.id, order=None).values('price').\
                                     annotate(tickets_number=Count('price')).\
                                     values('price__price', 'price__ticket_type__name', 'tickets_number')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tickets = serializers.SlugRelatedField(many=True, read_only=False, queryset=Ticket.objects.filter(order=None),
                                           slug_field='serial_number')
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'


class Tickets(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Ticket.objects.all()
        request = self.context.get('request', None)
        queryset = queryset.filter(Q(order__owner=request.user) | Q(order=None))
        return queryset


class DetailOrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tickets = Tickets(many=True, read_only=False, slug_field='serial_number')
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']
