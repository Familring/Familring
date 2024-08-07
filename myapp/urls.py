from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('today_question/', views.today_question, name='today_question'),
    path('questions/', views.questions, name='questions'),
    path('questions/<int:question_id>/answers/', views.question_answers, name='question_answers'),
]
