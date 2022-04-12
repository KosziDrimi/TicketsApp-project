from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

from .models import Event, Order, Price, Ticket, TicketType
from .serializers import DetailEventSerializer, DetailOrderSerializer, EventSerializer, OrderSerializer, UserSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class TicketTypeView(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TicketType.SimpleSerializer


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = EventSerializer
    serializer_action_class = {'retrieve': DetailEventSerializer, 'update': DetailEventSerializer}

    def get_serializer_class(self):
        try:
            return self.serializer_action_class[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class PriceView(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = Price.SimpleSerializer


class OrderView(viewsets.ModelViewSet):
    filterset_fields = ('owner',)
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = OrderSerializer
    serializer_action_class = {'retrieve': DetailOrderSerializer, 'update': DetailOrderSerializer}

    def get_queryset(self):
        orders = Order.objects.all()
        orders = [order.delete() for order in orders if order.is_valid is False]

        if self.request.user.is_staff:
            return Order.objects.all()

        return self.request.user.orders.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        try:
            return self.serializer_action_class[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.filter(order=None)
    permission_classes = [IsAdminUser | ReadOnly]
    serializer_class = Ticket.SimpleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('price__event', 'price__ticket_type')


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
