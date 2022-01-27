from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('types', views.TicketTypeView)
router.register('events', views.EventView)
router.register('prices', views.PriceView)
router.register('orders', views.OrderView)
router.register('tickets', views.TicketView)

urlpatterns = [
    path('', include(router.urls))
]
