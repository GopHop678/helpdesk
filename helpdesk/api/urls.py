from django.urls import path
from .views import *

urlpatterns = [
    path('request/<int:pk>', RequestAPIView.as_view(), name='request_details'),
    path('files/<int:pk>', UploadedFilesAPIView.as_view(), name='request_files'),
]
