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
        fields = ('id', 'title', 'therapist_id', 'duration', 'questions')

class PerformanceSerializer(ModelSerializer):
    quiz_title = serializers.SerializerMethodField('get_quiz_title')
    question = serializers.SerializerMethodField('get_question')
    answer = serializers.SerializerMethodField('get_answer')
    client_id = serializers.SerializerMethodField('get_client_id')

    class Meta:
        model = Performance
        fields = ('id', 'client_id', 'event_id', 'quiz_title', 'question', 'answer', 'is_correct')

    def get_quiz_title(self, obj):
        return obj.quiz.title
    
    def get_question(self, obj):
        return obj.question.question
    
    def get_answer(self, obj):
        if obj.answer:
            return obj.answer.answer

    def get_client_id(self, obj):
        if obj.answer:
            return obj.client.client_id

class ResultSerializer(ModelSerializer):
    quiz_title = serializers.SerializerMethodField('get_quiz_title')
    quiz_category = serializers.SerializerMethodField('get_quiz_category')
    total_questions = serializers.SerializerMethodField('get_total_questions')
    client_id = serializers.SerializerMethodField('get_client_id')

    class Meta:
        model = Result
        fields = ('id', 'room_id', 'quiz_title', 'quiz_category', 'client_id', 'total_questions', 'correct_answers', 'wrong_answers', 'time_taken', 'time_over')
    
    def get_quiz_title(self, obj):
        return obj.quiz.title

    def get_quiz_category(self, obj):
        return obj.quiz.category
    
    def get_total_questions(self, obj):
        return obj.correct_answers + obj.wrong_answers

    def get_client_id(self, obj):
        return obj.client.client_id