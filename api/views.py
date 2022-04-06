from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from datetime import timedelta
from django.utils.timezone import localtime

from .models import TicketType, Event, Price, Order, Ticket
from .serializers import EventSerializer, OrderSerializer, UserSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class TicketTypeView(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketType.SimpleSerializer
    permission_classes = [IsAdminUser]


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser|ReadOnly]


class PriceView(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = Price.SimpleSerializer
    permission_classes = [IsAdminUser]


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filterset_fields = ('owner',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        return self.request.user.orders.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if ((localtime() - instance.order_datetime) > timedelta(minutes=15)) and not instance.is_paid:
            serializer.save(ticket=[])
            raise APIException(detail='In order to stay valid the reservation needs to be paid within 15 minutes.')


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.filter(orders=None)
    serializer_class = Ticket.SimpleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event', 'price__ticket_type')
    permission_classes = [IsAdminUser | ReadOnly]


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
