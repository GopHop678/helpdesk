from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Worker, UploadedFile, Request


def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def board_view(request):
    worker = Worker.objects.get(user=request.user)
    if worker.role == 'admin':
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(sender=worker)
    requests = requests.order_by('-request_date')
    return render(request, 'requests.html', {
        'requests': requests,
    })


@transaction.atomic
@login_required(login_url='login')
def new_request(request):
    if request.method == 'POST':
        worker = Worker.objects.get(user=request.user)
        category = request.POST.get('category')
        place = request.POST.get('place')
        request_text = request.POST.get('request_text')
        new_request_obj = Request(
            category=category,
            status='WORKING',
            place=place,
            request_text=request_text,
            request_date=datetime.now(),
            sender=worker
        )
        new_request_obj.save()

        uploaded_files = request.FILES.getlist('files')
        if uploaded_files:
            for file in uploaded_files:
                 UploadedFile(
                    request=new_request_obj,
                    file=file,
                    file_type=file.name.split('.')[-1]
                ).save()

        return redirect('board')
    return render(request, 'new_request.html')


@login_required(login_url='login')
def delete_file(request, file_id):
    worker = Worker.objects.get(user=request.user)
    file_to_delete = UploadedFile.objects.get(id=file_id)
    test = file_to_delete.question.test

    if worker.role in ['admin']:
        pass
    else:
        return render(request, '403.html', {'messages': ['В доступе отказано']})

    if request.method == 'POST':
        if request.POST['confirm'] == 'yes':
            file_to_delete.delete()
            return redirect('edit_question', test_id=test.id, question_id=file_to_delete.question.id)
        elif request.POST['confirm'] == 'no':
            return redirect('edit_question', test_id=test.id, question_id=file_to_delete.question.id)
    return render(request, 'delete_confirmation.html', {'object': file_to_delete.file})


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        worker = Worker.objects.filter(full_name=full_name)
        if worker.exists():
            user = worker[0].user
            if not user.is_active:
                return render(request, 'login.html', {
                    'errors': ['Учетная запись неактивна. Обратитесь к администратору']
                })

            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('board')
            else:
                return render(request, 'login.html', {
                    'errors': ['Неправильное имя пользователя или пароль']
                })
        else:
            return render(request, 'login.html', {
                'errors': ['Пользователь с таким именем не существует']
            })
    return render(request, 'login.html')


@csrf_protect
def user_signup(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        if Worker.objects.filter(full_name=full_name).exists():
            return render(request, 'signup.html', {
                'errors': ['Пользователь с таким именем уже существует']
            })

        username = f'user_{len(User.objects.all())+1}'
        password1 = request.POST.get('password')
        password2 = request.POST.get('password_confirmation')
        if password1 == password2:
            new_user = User.objects.create_user(
                username=username,
                password=password1,
                is_active=False
            )
            login(request, new_user)
            Worker(user=new_user, full_name=full_name).save()
            return redirect('board')
        else:
            return render(request, 'signup.html', {
                'errors': ['Пароли не совпадают']
            })
    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')
