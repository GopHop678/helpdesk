from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import viewsets
from main.models import Worker, UploadedFile, Request
from .serializers import ProductSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = ProductSerializer