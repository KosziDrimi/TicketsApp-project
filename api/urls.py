from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('types', views.TicketTypeView)
router.register('events', views.EventView)
router.register('prices', views.PriceView)
router.register('orders', views.OrderView, basename='order')
router.register('tickets', views.TicketView)
router.register('users', views.UserView)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
