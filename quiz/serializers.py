from typing_extensions import Required
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(source = 'get_answers', many = True, required = False)

    class Meta:
        model = Question
        fields = ('id', 'question', 'difficulty', 'answers')

class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(source = 'get_questions', many = True, required = False)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'therapist_id', 'questions')

class PerformanceSerializer(ModelSerializer):
    quiz_title = serializers.SerializerMethodField('get_quiz_title')
    question = serializers.SerializerMethodField('get_question')
    answer = serializers.SerializerMethodField('get_answer')

    class Meta:
        model = Performance
        fields = ('id', 'user_id', 'event_id', 'quiz_title', 'question', 'answer', 'is_correct')

    def get_quiz_title(self, obj):
        return obj.quiz.title
    
    def get_question(self, obj):
        return obj.question.question
    
    def get_answer(self, obj):
        return obj.answer.answer
