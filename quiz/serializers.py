from typing_extensions import Required
from rest_framework.serializers import ModelSerializer
from .models import *

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(source = 'answer_set', many = True, required = False)

    class Meta:
        model = Question
        fields = ('id', 'question', 'difficulty', 'answers')

class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(source = 'question_set', many = True, required = False)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'therapist_id', 'questions')
