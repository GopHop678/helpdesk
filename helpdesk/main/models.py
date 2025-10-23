from django.db import models
from django.contrib.auth.models import User
import datetime


def time_now():
    return datetime.datetime.now()


def upload_path(instance, filename):
    request_id = instance.request.id
    return f'uploads/{request_id}/{filename}'


class Worker(models.Model):
    worker_roles = [
        ('admin', 'Администратор'),
        ('worker', 'Сотрудник'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=worker_roles, default='worker')
    full_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f'{self.full_name}'


class Request(models.Model):
    request_types = [
        ('PRINTER', 'Принтер'),
        ('SOFTWARE', 'Программа'),
        ('HARDWARE', 'Компьютер'),
        ('ETC', 'Другое'),
    ]
    status_choices = [
        ('WORKING', 'В работе'),
        ('COMPLETED', 'Выполнено'),
        ('REJECTED', 'Отклонено'),
    ]

    request_text = models.CharField(max_length=2048, null=True, blank=True,
                                    default='Описание отсутствует')
    place = models.CharField(max_length=128, null=False)
    request_date = models.DateTimeField(null=False)
    sender = models.ForeignKey(Worker, on_delete=models.CASCADE)
    category = models.CharField(choices=request_types)
    status = models.CharField(choices=status_choices, default='WORKING')

    def __str__(self):
        return f'{self.request_text[:50]} от {self.sender}'


class UploadedFile(models.Model):
    file_types = [
        ('docx', 'Word'),
        ('xlsx', 'Excel'),
        ('pdf', 'PDF'),
        ('png', 'Картинка PNG'),
        ('jpg', 'Картинка JPG'),
        ('jpeg', 'Картинка JPEG'),
    ]

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    file_type = models.CharField(choices=file_types)
    file = models.FileField(upload_to=upload_path)

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.request}.{self.file_type}'
