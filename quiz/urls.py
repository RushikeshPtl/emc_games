from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('create_quiz/', QuizView.as_view(), name='create_quiz'),
    path('add_question/', QuestionView.as_view(), name='add_question'),
    path('get_quiz_list/', GetQuizList.as_view(), name='get_quiz_list'),
    path('get_quiz/<id>', GetQuiz.as_view(), name='get_quiz'),
    path('get_questions/<quiz_id>', GetQuestions.as_view(), name='get_questions'),
    path('performance/', PerformanceView.as_view(), name = 'submit_performance'),
    path('performance/<quiz_id>', PerformanceView.as_view(), name = 'get_performance')
]