from django.urls import path
from .views import *

urlpatterns = [
    path('request/<int:pk>', RequestAPIView.as_view(), name='request_details'),
    path('request/<int:pk>/change_status', ChangeRequestStatusAPIView.as_view(), name='change_status'),
    path('request/<int:pk>/files', UploadedFilesAPIView.as_view(), name='request_files'),
]
