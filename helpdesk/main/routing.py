from django.urls import path
from .consumers import WSConsumer


ws_urlpatterns = [
    path('ws/board/', WSConsumer.as_asgi())
]
