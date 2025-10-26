from django.urls import path
from .consumers import WSConsumer


ws_urlpatterns = [
    path('ws/tmp/', WSConsumer.as_asgi())
]
