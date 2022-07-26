from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core import serializers
import pdb
from .serializers import *
# Create your views here.

class QuizView(APIView):
    def get(self, request):
        return render(request, 'create_quiz.html')

    def post(self, request):
        quiz = Quiz(
            title = request.data.get('title'),
            category = request.data.get('category'),
            therapist_id = request.data.get('therapist_id')
        )
        quiz.save()
        quiz_json = serializers.serialize('json', [quiz, ])
        return JsonResponse({"quiz" : quiz_json}, status=200)


class QuestionView(APIView):
    def post(self, request):
        question = Question(
            question = request.data.get('question'),
            difficulty = request.data.get('difficulty'),
            quiz_id = request.data.get('quiz_id')
        )
        question.save()
        for i in range(1, 5):
            if request.data.get('answer'+str(i)):
                answer = Answer(
                    answer = request.data.get('answer'+str(i)).get('answer'),
                    is_correct = request.data.get('answer'+str(i)).get('is_correct'),
                    question_id = question.id
                )
                answer.save()
            else:
                break
        return JsonResponse({"Question" : "Added"}, status=200)

class GetQuiz(APIView):
    def get(self, request, id):
        quiz = Quiz.objects.filter(pk=id).first()
        if quiz:
            quiz_data = QuizSerializer(quiz)
            return Response(quiz_data.data)
        else:
            return Response("Please enter valid quiz ID......")

# class PerformanceView(APIView):
#     def post(self, request):
#         user_id = request.data.get('User ID')
#         event_id = request.data.get('Event ID')
#         quiz_id = request.data.get('Quiz ID')
#         question_id = request.data.get('Question ID')
#         answer_id = request.data.get('Answer ID')
#         is_correct = Answer.objects.get(pk = answer_id).is_correct
#         Performance.objects.create(user_id = user_id, event_id = event_id, quiz_id = quiz_id, question_id = question_id, answer_id = answer_id, is_correct = is_correct)
#         return Response("Performance Recorded......................")
    
#     def get(self, request, quiz_id):
#         user_id = request.data.get("user_id")
#         event_id = request.data.get("event_id")
#         performance = Performance.objects.filter(quiz_id = quiz_id, user_id = user_id, event_id = event_id)
#         total_questions = performance.count()
#         correct_questions = performance.filter(is_correct = True).count()

