from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import TicketType, Event, Price, Order, Ticket
from .serializers import TicketTypeSerializer, EventSerializer, PriceSerializer, OrderSerializer, TicketSerializer,\
                         UserSerializer


class TicketTypeView(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PriceView(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        return self.request.user.orders.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event', 'price__ticket_type')


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
