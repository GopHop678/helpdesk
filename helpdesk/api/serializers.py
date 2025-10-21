from rest_framework import serializers
from main.models import Worker, Request, UploadedFile


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            'full_name'
        ]


class RequestSerializer(serializers.ModelSerializer):
    sender = WorkerSerializer()

    class Meta:
        model = Request
        fields = [
            'id',
            'request_text',
            'request_date',
            'sender',
            'category',
            'place',
            'status',
        ]



class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = [
            'file',
            'file_type',
        ]
