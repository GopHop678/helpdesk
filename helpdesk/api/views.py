from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Worker, UploadedFile, Request
from .serializers import RequestSerializer, UploadedFilesSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class RequestAPIView(APIView):
    def get(self, request, pk):
        request_obj = Request.objects.get(pk=pk)
        serializer = RequestSerializer(request_obj, many=False)
        return Response(serializer.data, status=200)


class DoneRequestsAPIView(APIView):
    def get(self, request):
        request_obj = Request.objects.filter(status__in=['COMPLETED', 'REJECTED'])
        serializer = RequestSerializer(request_obj, many=True)
        return Response(serializer.data, status=200)


class ChangeRequestStatusAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, pk):
        try:
            request_obj = Request.objects.get(pk=pk)
            if request_obj.status == 'WORKING':
                new_status = request.data
                request_obj.status = new_status
                request_obj.save()
                return Response({'request_id': request_obj.id}, status=200)
            else:
                raise Exception
        except Exception as e:
            print(e)
            return Response({'response': 'error'}, status=400)


class UploadedFilesAPIView(APIView):
    def get(self, request, pk):
        files = UploadedFile.objects.filter(request__id=pk)
        serializer = UploadedFilesSerializer(files, many=True)
        return Response(serializer.data, status=200)
