from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
import datetime
import random
from .models import Worker, UploadedFile, Request


def get_role(user):
    worker = Worker.objects.get(user=user)
    if worker.role == 'admin':
        return 'admin'
    if worker.role == 'worker':
        return 'worker'


# @login_required(login_url='login')
# def form_protocol_file(request, test_id, result_id):
#     role = get_role(request.user)
#     worker = Worker.objects.get(user=request.user)
#     test = Test.objects.get(id=test_id)
#     if role in ['admin']:
#         pass
#     elif role in ['curator'] and test.curator == worker:
#         pass
#     else:
#         return render(request, '403.html', {'messages': ['В доступе отказано']})
#
#     result = Result.objects.get(id=result_id)
#     attempt_questions = AttemptQuestion.objects.filter(result=result).values_list('question', flat=True)
#     test_questions = Question.objects.filter(id__in=attempt_questions, test__id=test_id)
#     if not test_questions.exists():  # old tests compatibility
#         test_questions = Question.objects.filter(test=test)
#     variants = AnswerVariant.objects.filter(question__test=test, is_correct=True)
#     pairs = AnswerPair.objects.filter(question__test=test)
#     open_answer = AnswerOpen.objects.filter(question__test=test)
#     test_questions = test_questions.prefetch_related(
#         Prefetch('answervariant_set', queryset=variants, to_attr='variants')
#     )
#     test_questions = test_questions.prefetch_related(
#         Prefetch('answerpair_set', queryset=pairs, to_attr='pairs')
#     )
#     test_questions = test_questions.prefetch_related(
#         Prefetch('answeropen_set', queryset=open_answer, to_attr='open_answer')
#     )
#     user_answers = UserAnswer.objects.filter(question__test=test, result=result)
#     max_score = len(test_questions)
#
#     buffer = io.BytesIO()
#     time_spent = result.finish_date - result.start_date
#     result_score = int(result.result) if round(result.result, 5) == int(result.result) \
#         else round(result.result, 5)
#     header = f'''Тестируемый: {user_answers[0].result.worker.full_name}
# Подразделение: {user_answers[0].result.worker.departament}
# Тест: {test_questions[0].test.test_name}
# Набрано баллов: {result_score}
# Максимум баллов: {max_score}
# Дата прохождения: {result.finish_date.day}.{result.finish_date.month}.{result.finish_date.year}
# Тест пройден: {'Да' if result.is_passed else 'Нет'}
# Затраченное время: {time_spent.seconds//3600}:{time_spent.seconds//60%60}:{time_spent.seconds%60}'''
#
#     table = [[header], ['№', 'Текст вопроса', 'Ответ пользователя', 'Правильный ответ', 'Верно']]
#     font_path = settings.BASE_DIR / 'static/fonts/DejaVuSerif.ttf'
#     pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
#     styles = getSampleStyleSheet()
#     styles['Normal'].fontName = 'DejaVuSerif'
#     styles['Normal'].fontSize = 8
#     for i, question in enumerate(test_questions):
#         question_type = get_question_type(question)
#         row = list()
#         row.append(i+1)
#
#         user_answer_cell = ''
#         correct_answer_cell = ''
#         if question_type == 'pairs':
#             pairs = AnswerPair.objects.filter(question=question)
#             for pair in pairs.order_by('left_part'):
#                 correct_answer_cell += f'{pair.left_part} - {pair.right_part};\n'
#             for answer in user_answers.filter(question=question).order_by('left_part'):
#                 user_answer_cell += f'{answer.left_part} - {answer.right_part};\n'
#         elif question_type == 'variants':
#             correct_answer = AnswerVariant.objects.filter(question=question, is_correct=True)
#             correct_answer_cell += correct_answer[0].answer_text
#             user_answer_obj = user_answers.filter(question=question)
#             if user_answer_obj:
#                 user_answer_cell += f'{user_answer_obj[0].simple_answer}'
#             else:
#                 user_answer_cell += '-'
#         elif question_type == 'open':
#             open_answer = AnswerOpen.objects.filter(question=question)
#             correct_answer_cell += open_answer[0].correct_answer
#             user_answer_obj = user_answers.filter(question=question)
#             if user_answer_obj:
#                 user_answer_cell += f'{user_answer_obj[0].simple_answer}'
#             else:
#                 user_answer_cell += '-'
#
#         row.append(Paragraph(question.question_text, styles['Normal']))
#         row.append(Paragraph(user_answer_cell, styles['Normal']))
#         row.append(Paragraph(correct_answer_cell, styles['Normal']))
#         row.append('Да' if user_answer_cell.lower() == correct_answer_cell.lower() else 'Нет')
#         table.append(tuple(row))
#
#     pdf_file = SimpleDocTemplate(buffer, pagesize=A4,
#                                  rightMargin=40, leftMargin=40, topMargin=20, bottomMargin=40)
#     table = Table(table, colWidths=[30, 150, 160, 160, 40])
#     style = TableStyle([
#         ('SPAN', (0, 0), (-1, 0)),
#         ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ('FONTSIZE', (1, 1), (-1, -1), 8),
#     ])
#     table.setStyle(style)
#     elements = [table]
#     pdf_file.build(elements)
#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = \
#         f'attachment; filename="protocol_{result.test.id}_{result.worker.id}.pdf"'
#     return response


def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def board_view(request):
    worker = Worker.objects.get(user=request.user)
    role = get_role(request.user)
    if role == 'admin':
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(sender=worker)
    requests = requests.order_by('-request_date')
    return render(request, 'requests.html', {
        'requests': requests,
    })


@login_required(login_url='login')
def new_request(request):
    if request.method == 'POST':
        category = request.GET.get('category')
        place = request.GET.get('place')
        request_text = request.GET.get('request_text')
        files = request.GET.get('files')
        return redirect('board')
    return render(request, 'new_request.html')


@login_required(login_url='login')
def delete_file(request, file_id):
    role = get_role(user=request.user)
    worker = Worker.objects.get(user=request.user)
    file_to_delete = UploadedFile.objects.get(id=file_id)
    test = file_to_delete.question.test

    if role in ['admin']:
        pass
    elif role in ['curator'] and test.curator == worker:
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
            user = authenticate(request, username=worker[0].user.username, password=password)
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

        username = f'user_{len(User.objects.all())}'
        password1 = request.POST.get('password')
        password2 = request.POST.get('password_confirmation')
        if password1 == password2:
            new_user = User.objects.create_user(
                username=username,
                password=password1,
                # is_active=False
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
