from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Worker, UploadedFile, Request
from .serializers import RequestSerializer, UploadedFilesSerializer


class RequestAPIView(APIView):
    def get(self, request, pk):
        request_obj = Request.objects.get(pk=pk)
        serializer = RequestSerializer(request_obj, many=False)
        return Response(serializer.data, status=200)


class ChangeRequestStatusAPIView(APIView):
    def put(self, request, pk):
        try:
            new_status = request.data.get('new_status')
            request_obj = Request.objects.get(pk=pk)
            request_obj.status = new_status
            request_obj.save()
            return Response({'response': 'success'}, status=200)
        except:
            return Response({'response': 'error'}, status=400)


class UploadedFilesAPIView(APIView):
    def get(self, request, pk):
        files = UploadedFile.objects.filter(request__id=pk)
        serializer = UploadedFilesSerializer(files, many=True)
        return Response(serializer.data, status=200)
