from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('board', board_view, name='board'),
    path('board/new', new_request, name='new_test'),
    path('signup', user_signup, name='signup'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('download_pdf/<int:request_id>', index, name='download_pdf'),
]
